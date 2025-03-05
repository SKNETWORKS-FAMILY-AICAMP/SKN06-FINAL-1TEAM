import json
from rapidfuzz import process, fuzz
from main.prediction.database import load_corp_mapping,get_corp_code,get_financial_data,get_economic_indicators,get_company_profile
from main.prediction.preprocess import preprocess_financial_data
from main.prediction.prediction import predict_revenue
from main.prediction.outlook import determine_outlook
from main.prediction.utils import format_korean_currency



def get_candidate_companies(company_name: str):
    """
    회사명을 기반으로 가장 유사한 회사 목록을 반환
    """
    candidates = process.extract(company_name, load_corp_mapping().keys(), scorer=fuzz.WRatio, limit=5)
    return [c[0] for c in candidates if c[1] > 90]  # 70점 이상만 반환

def get_valid_company(extracted_company: str) -> str:
    """
    추출된 기업명을 DB에서 검색하여 데이터가 있으면 그대로 사용하고,
    없으면 유사한 기업명을 자동 추천하고, 필요시 사용자 입력을 받음.
    """
    corp_code = get_corp_code(extracted_company)
    
    # 정확한 이름이 DB에 있으면 그대로 반환
    if corp_code:
        return extracted_company
    
    # DB에 없는 경우 유사한 기업명 추천
    candidates = get_candidate_companies(extracted_company)
    
    if candidates:
        best_match = candidates[0]  # 가장 유사한 기업명 선택
        print(f"🔍 입력하신 '{extracted_company}'와 가장 유사한 기업: {best_match}")
        
        # 유사도가 높으면 자동 선택
        if process.extractOne(extracted_company, [best_match], scorer=fuzz.WRatio)[1] > 85:
            print(f"'{best_match}'를 자동 선택합니다.")
            return best_match
        
        # 유사도 낮으면 사용자 입력 요청
        print(f"📌 유사한 기업 목록: {', '.join(candidates)}")
        new_company = input("올바른 기업명을 입력해주세요 (자동 추천을 원하면 Enter): ").strip()
        
        return new_company if new_company else best_match  # 사용자가 입력하지 않으면 자동 추천
    else:
        print(f"🚨 '{extracted_company}'과 유사한 기업을 찾을 수 없습니다.")
        return extracted_company
    


def extract_company_and_year(user_input,llm):
    """
    사용자의 질문에서 기업명과 연도를 추출하고 corp_code를 매칭하는 함수
    """
    extraction_prompt = f"""
    사용자의 질문에서 기업명과 연도를 정확하게 추출하세요.
    질문: "{user_input}"
    
    형식:
    {{
        "기업명": ["기업1", "기업2"],
        "연도": "연도 (없으면 최신 연도 2024로 설정)"
    }}
    """

    # LLM을 활용해 기업명과 연도 추출 (LLM 연동 필요)
    extraction_result = llm.invoke(extraction_prompt).content.strip()

    try:
        extracted_data = json.loads(extraction_result)
        extracted_names = extracted_data.get("기업명", [])
        if not isinstance(extracted_names, list):
            extracted_names = [extracted_names]

        year = int(extracted_data.get("연도", 2024))  # 연도가 없으면 2024 기본값
    except (json.JSONDecodeError, ValueError):
        return "❌ 기업명 또는 연도를 정확히 추출할 수 없습니다.", None

    # corp_code 매칭
    matched_companies = []
    for name in extracted_names:
        valid_company = get_valid_company(name)
        corp_code = get_corp_code(valid_company)

        if corp_code:
            matched_companies.append((valid_company, corp_code))  # (기업명, corp_code) 튜플 저장
        else:
            matched_companies.append((valid_company, None))  # 매칭 실패
            print(f"🚨 '{name}'과 일치하는 기업을 찾을 수 없음")

    return matched_companies, year



def company_forecast(stock_name, year, llm):
    """
    기업의 미래 전망을 예측하는 함수.
    
    Args:
        stock_name (str): 기업명
        year (int): 예측 연도
        conn: MySQL 데이터베이스 연결 객체
    
    Returns:
        str: 예측 결과 리포트
    """
    corp_code = get_corp_code(stock_name)
    if not corp_code:
        return f"❌ '{stock_name}'의 corp_code를 찾을 수 없습니다."

    # ✅ 1. 재무 데이터 조회
    financials = get_financial_data(corp_code)
    
    if financials is None or all(df.empty for df in financials.values()):
        return f"❌ {stock_name}({corp_code})의 {year}년 재무 데이터를 찾을 수 없습니다."

    # ✅ 3. 데이터 전처리

    X_new = preprocess_financial_data(financials)[0]

    outlook_df = preprocess_financial_data(financials)[1]


    # # ✅ 4. 모델 로드
    # MODEL_PATH = os.path.join("예측모델", "linear_regression_model.pkl")
    # model = joblib.load(MODEL_PATH)

    # ✅ 5. 예측 결과
    # 예측 전에 corp_code 컬럼 제거
    X_new = X_new.drop(columns=["corp_code"], errors="ignore")

    predicted_revenue = predict_revenue(X_new)

    formatted_revenue = f"{format_korean_currency(predict_revenue(X_new))}"  # 예측 매출액 변환

    # ✅ 7. 경제 지표 가져오기
    economic_data = get_economic_indicators()
    economic_data_year = economic_data[economic_data["year"] == year]
    exchange_rate = round(economic_data_year["Exchange Rate (USD/KRW)"].values[0], 2)
    oil_price = round(economic_data_year["WTI Crude Oil Price"].values[0], 2)

    # ✅ 8. 기업 개요 및 최근 사업 동향
    company_profile = get_company_profile(corp_code)  
    business_summary = llm.invoke(f"{company_profile} 기반으로 최근 사업 동향을 3줄 요약해 주세요.").content.strip()

    # ✅ 9. 재무 지표 계산
    try:
        sales_growth_rate = ((predicted_revenue-outlook_df["ifrs-full_Revenue"].values[0]) / outlook_df["ifrs-full_Revenue"].values[0]) * 100
        operating_margin = (outlook_df["dart_OperatingIncomeLoss"].values[0] /
                            (outlook_df["ifrs-full_Revenue"].values[0])) * 100
        debt_ratio = (X_new["ifrs-full_Liabilities"].values[0] / X_new["ifrs-full_Equity"].values[0]) * 100
        liquidity_ratio = (X_new["ifrs-full_CurrentAssets"].values[0] / X_new["ifrs-full_CurrentLiabilities"].values[0]) * 100
    except KeyError as e:
        print(f"❌ KeyError: {e} - 해당 지표가 없음")
        return f"❌ {stock_name}({corp_code})의 {year}년 재무 데이터를 충분히 확보하지 못했습니다."
    
    # load the determine_outlook func

    outlook = determine_outlook(operating_margin, debt_ratio, sales_growth_rate, liquidity_ratio)
    
    report = f"""
    📢 **{stock_name}({corp_code}) {year}년 전망 보고서**

    📑 **미래 전망**: {outlook}
    
    💰 **예측 매출액**: {formatted_revenue} 원

    📊 **전망 예측 고려 요인**
    - 🌍 **거시경제지표**
      - 환율 변동성 (평균): {exchange_rate} 원/USD
      - 원유 가격 (평균): {oil_price} USD/배럴

    - 🏢 **기업 동향**
      {business_summary}

    - 📈 **기업 재무 상태**
      - 매출성장률(예측 매출액 기준): {sales_growth_rate:.2f}%
      - 영업이익률: {operating_margin:.2f}%
      - 부채비율: {debt_ratio:.2f}%
      - 유동비율: {liquidity_ratio:.2f}%

    💡 **전망 요약**
    - {stock_name}의 {year}년 매출은 **{formatted_revenue} 원**으로 예측됨.
    - 거시경제 지표(환율, 유가) 및 기업 동향에 따라 실적 변동 가능성이 있음.
    - 투자 시 **재무 안정성과 시장 트렌드를 고려**하는 것이 중요함.
    """

    return report



def interactive_forecast(user_input: str, llm):
    """
    사용자 입력을 받아 기업명과 연도를 추출하고, 해당 기업의 미래 전망 보고서를 생성
    """


    # ✅ 기업명 & 연도 추출
    matched_companies, year = extract_company_and_year(user_input, llm)
    
    if matched_companies == "❌ 기업명 또는 연도를 정확히 추출할 수 없습니다.":
        return matched_companies
    response = ""
    for company_name, corp_code in matched_companies:
        if corp_code:
            response = company_forecast(company_name, year,llm)
            return response
        else:
            print(f"❌ '{company_name}'의 corp_code를 찾을 수 없습니다.\n")
            return f"{company_name}의 corp_code를 찾을 수 없습니다.\n"
        
