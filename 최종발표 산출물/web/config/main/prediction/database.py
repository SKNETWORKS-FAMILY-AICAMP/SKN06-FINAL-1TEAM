import pymysql,os,requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )


def load_corp_mapping():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        query = "SELECT corp_code, stock_name FROM company_list"
        cursor.execute(query)
        result = cursor.fetchall()
    
    corp_mapping = {row["stock_name"]: row["corp_code"] for row in result}
    conn.close()
    return corp_mapping


def get_corp_code(stock_name):
    return load_corp_mapping().get(stock_name, None)  # 매칭되지 않으면 None 반환


def get_company_profile(corp_code):
    query = "SELECT corp_code, stock_name a FROM company_list WHERE corp_code = %s"

    conn = get_db_connection()
    company_profile = None
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (corp_code,))
            company_profile = cursor.fetchone()
    except Exception as e:
        print(f"회사 프로필 조회 중 오류 발생: {e}")
    finally:
        conn.close()
        
    return company_profile


def get_financial_data(corp_code):
    """
    특정 기업의 재무 데이터를 조회하여 DataFrame으로 변환하는 함수.
    
    Args:
        corp_code (str): 기업의 코드
        conn: MySQL 데이터베이스 연결 객체

    Returns:
        dict: 손익계산서(IS), 재무상태표(BS), 포괄손익계산서(CIS) 데이터가 포함된 사전.
    """
    queries_ofs = {
        "is": "SELECT corp_code, concept_id, 2023amount, 2022amount, 2021amount FROM single_is WHERE corp_code = %s",
        "bs": "SELECT corp_code, concept_id, 2023amount, 2022amount, 2021amount FROM single_bs WHERE corp_code = %s",
        "cis": "SELECT corp_code, concept_id, 2023amount, 2022amount, 2021amount FROM single_cis WHERE corp_code = %s"
    }

    queries_cfs = {
        "is": "SELECT corp_code, concept_id, 2023amount, 2022amount, 2021amount FROM connection_is WHERE corp_code = %s",
        "bs": "SELECT corp_code, concept_id, 2023amount, 2022amount, 2021amount FROM connection_bs WHERE corp_code = %s",
        "cis": "SELECT corp_code, concept_id, 2023amount, 2022amount, 2021amount FROM connection_cis WHERE corp_code = %s"
    }

    conn = get_db_connection()
    financial_data = {"ofs": {}, "cfs": {}}

    try:
        with conn.cursor() as cursor:
            for key, query in queries_ofs.items():
                cursor.execute(query, (corp_code,))
                result = cursor.fetchall()
                financial_data["ofs"][key] = pd.DataFrame(result, columns=["corp_code", "concept_id", "2023amount", "2022amount", "2021amount"])

            for key, query in queries_cfs.items():
                cursor.execute(query, (corp_code,))
                result = cursor.fetchall()
                financial_data["cfs"][key] = pd.DataFrame(result, columns=["corp_code", "concept_id", "2023amount", "2022amount", "2021amount"])

        return financial_data
    finally:
        conn.close()
    

def get_economic_indicators():
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    FRED_BASE_URL = os.getenv("FRED_BASE_URL")
    FRED_INDICATORS = {
        "Exchange Rate (USD/KRW)": "DEXKOUS",
        "WTI Crude Oil Price": "DCOILWTICO"
    }

    start_year = 2020
    end_year = 2024

    economic_data = {"year": [], "indicator": [], "value": []}
    for indicator_name, series_id in FRED_INDICATORS.items():
        url = f"{FRED_BASE_URL}?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()["observations"]
            
            for entry in data:
                year = int(entry["date"][:4])
                if start_year <= year <= end_year:
                    economic_data["year"].append(year)
                    economic_data["indicator"].append(indicator_name)
                    economic_data["value"].append(float(entry["value"]) if entry["value"] != "." else None)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {indicator_name} 데이터 요청 실패: {e}")

    df_econ = pd.DataFrame(economic_data)
    df_econ["year"] = pd.to_datetime(df_econ["year"], format="%Y").dt.year  # 'year'를 datetime으로 변환
    df_econ_avg = df_econ.groupby(["year", "indicator"])["value"].mean().reset_index()
    
    df_econ_pivot = df_econ_avg.pivot(index="year", columns="indicator", values="value").reset_index()
    return df_econ_pivot


def get_news():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        query = "SELECT sentiment_gpt, pub_date FROM cleaned_news_data"
        cursor.execute(query)
        result = cursor.fetchall()

    conn.close()
    return result