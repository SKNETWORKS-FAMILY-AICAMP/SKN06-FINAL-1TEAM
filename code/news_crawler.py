############################################################################
# 1st_crawler.py + 2nd_cralwer.py 로, 본문까지 모두 포함하여 크롤링하는 크롤러
# 크롤링 후, 첫 번째 DB에 저장.
############################################################################

# 1st DB: title_org, pub_date_org, newspaper_org, content_org, link_org (id, link_org_hash)
# 2nd DB: title, pub_date, newspaper, content, link (id, link_hash)

# 본문 길이가 50자 이하일 경우 저장하지 않음.

import re
import os
import time
import json
import random
import hashlib
import logging
import requests
import pymysql
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from db_utils import get_db_connection, safe_request


# [ 각 파일별 절대 경로 설정 ]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "news_parsing_config.json")
LOG_FILE = os.path.join(BASE_DIR, "news_crawler.log")


# [ 로깅 설정 ]
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    handlers = [
        logging.FileHandler(LOG_FILE, encoding="utf-8-sig"),
        # console 출력
        logging.StreamHandler()
    ]
)


# [ headers 전역 변수 설정 ]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.naver.com",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}


# [ 유틸리티(해시값) 생성 함수 ]
def generate_link_hash(link_org):
    """
    SHA-256 해시값을 생성하는 함수
    """
    return hashlib.sha256(link_org.encode('utf-8')).hexdigest()


# [ 날짜 변환 함수 ]
def parse_date(date_str):
    """
    날짜 문자열을 datetime 객체로 변환하는 함수.
    - "YYYY.MM.DD", "YYYY-MM-DD", "YYYY/MM/DD", "YYYY년 MM월 DD일" 형식 변환
    - 상대 시간을 현재 시각 기준으로 변환
    - 변환 실패 시 기본값 반환 (현재 시간 기준)
    """
    try:
        if isinstance(date_str, datetime):
            return date_str
        
        now = datetime.now()

        # 신문 지면 정보 필터링 (예: "14면 1단", "23면 1단")
        if re.match(r"^\d+면 \d+단$", date_str):
            logging.warning(f"신문 지면 정보로 날짜 파싱 불가: {date_str}. 해당 기사 스킵.")
            return None  # 기사 스킵

        # 상대적 시간 처리
        match = re.search(r'(\d+)', date_str)
        if "전" in date_str and match:
            value = int(match.group())
            if "초" in date_str:
                return now - timedelta(seconds=value)
            elif "분" in date_str:
                return now - timedelta(minutes=value)
            elif "시간" in date_str:
                return now - timedelta(hours=value)
            elif "일" in date_str:
                return now - timedelta(days=value)
            elif "주" in date_str:
                return now - timedelta(weeks=value)

        # 다양한 날짜 형식 처리
        date_formats = ["%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d", "%Y년 %m월 %d일"]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue  # 형식이 맞지 않으면 다음 형식으로 검사
        
        # 날짜 형식이 전혀 맞지 않을 경우 None 반환 → 기사 스킵
        logging.warning(f"유효하지 않은 날짜 형식: {date_str}. 해당 기사 스킵.")
        return None  

    except Exception as e:
        logging.error(f"날짜 변환 오류: {e} (입력 값: {date_str})")
        # 변환 실패 시 기사 스킵
        return None


# [ MySQL 저장 함수 ]
def save_news_db(title_org, newspaper_org, pub_date_org, content_org, link_org):
    """
    MySQL DB에 기사 데이터를 저장하는 함수
    이미 저장된 링크는 건너뛰어 중복 저장을 방지함.
    """
    try:
        conn = get_db_connection()
        if not conn:
            logging.error("DB 연결 실패로 해당 요청을 건너뜁니다.")
            return
        cursor = conn.cursor()

        # 링크 해시 생성
        link_org_hash = generate_link_hash(link_org)

        # 중복 방지(link_org_hash 기준)
        cursor.execute("SELECT id_org FROM news_data WHERE link_org_hash = %s", (link_org_hash,))
        existing = cursor.fetchone()

        if existing:
            logging.info(f"이미 저장된 기사(URL 중복): {link_org}")
            return
        
        # 데이터 저장
        sql = """
            INSERT INTO news_data (title_org, newspaper_org, pub_date_org, content_org, link_org, link_org_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title_org, newspaper_org, pub_date_org, content_org, link_org, link_org_hash))
        conn.commit()
        logging.info(f"기사 저장 완료: {title_org}")

    except Exception as e:
        logging.error(f"DB 저장 오류 ({title_org}): {e}")

    finally:
        cursor.close()
        conn.close()


# [ 설정 파일(news_parsing_config.json) 로드 ]
try:
    with open(CONFIG_FILE, "r", encoding="utf-8-sig") as f:
        news_config = json.load(f)
    logging.info("설정 파일(news_parsing_config.json) 로드 완료")
except Exception as e:
    logging.warning(f"설정 파일 로드 실패: {e}. 기본 설정을 사용합니다.")
    # 설정 파일 로드에 실패할 경우 DEFAULT_CONFIG에 정의한 기본 설정 사용 - 오류 줄이기
    news_config = {"news_sites": {}}


# [ 설정 파일 조회 함수 ]
def get_site_config(newspaper):
    """
    설정 파일(news_parsing_config.json)내 'news_sites' 항목에서
    신문사 이름(newspaper)과 일치하는 설정을 찾아 반환함.
    """
    return next((site for site in news_config.get("news_sites", {}).values() if site.get("name") == newspaper), None)


# [ 기사 본문 크롤링 함수 ]
def extract_article_text(link_org):
    """
    기사 본문을 추출하는 함수.
    HEADERS 변수의 User-Agent를 포함하여 직접 HTML을 다운로드한 후, newspaper3k 패키지에 전달함.
    """
    try:
        # requests로 HTML 직접 다운로드
        response = requests.get(link_org, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            logging.error(f"본문 추출 실패 ({link_org}): HTTP {response.status_code}")
            return ""
        
        # newspaper3k에 직접 HTML 전달
        article = Article(link_org, language='ko')
        article.download(input_html=response.text)
        article.parse()

        # 줄바꿈을 기준으로 문단 나누기
        paragraphs = article.text.split("\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return "\n".join(paragraphs)

    except Exception as e:
        logging.error(f"본문 추출 실패 ({link_org}): {e}")
        return ""


# [ 뉴스 크롤링 함수 ]
def fetch_naver_news():
    """
    - 1단계: 네이버 뉴스 검색 결과를 페이지(endpoint) 단위로 크롤링하여 네이버 뉴스 검색 결과에서 기사 제목, 작성일, 언론사, URL을 가져와 DB 저장.
    - 2단계: 기사 저장 직후 본문을 크롤링하여 DB 업데이트.
    - 기준 날짜(2025-01-01) 이전의 기사 조회 시 페이지 네비게이션 중단함.
    """
    base_url = "https://search.naver.com/search.naver"
    params = {
        "where": "news",  
        "query": "국내 자동차",
        "sm": "tab_opt",  
        "sort": "1",  # 최신순 정렬
        "photo": "0",  
        "field": "0",  
        "pd": "0", 
        "ds": "", "de": "",  
        "docid": "",
        "related": "0",
        "mynews": "0",
        "office_type": "0",
        "office_section_code": "0",
        "news_office_checked": "",
        "nso": "so:dd,p:all",
        "is_sug_officeid": "0",
        "office_category": "0",
        "service_area": "1"
    }

    base_date = datetime(2025, 1, 1)
    page = 0

    logging.info("뉴스 크롤링 시작")

    while True:
        # 페이지 네비게이션
        params["start"] = 1 + page * 10
        logging.info(f"페이지 {page+1} (start={params['start']}) 요청 중")
        response = safe_request(base_url, headers=HEADERS, params=params)
        if not response:
            break

        # HTML 직접 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 뉴스 검색 결과 기사 리스트 찾기
        articles = soup.find_all("div", class_="news_area")
        if not articles:
            logging.info("더 이상 수집할 뉴스 없음. 종료합니다.")
            break

        for article in articles:
            # 기사 제목 및 URL 추출
            title_tag = article.find("a", class_="news_tit")
            if not title_tag or not title_tag.get("href"):
                logging.warning("제목 또는 링크를 찾지 못했습니다. 스킵합니다.")
                continue
            title_org = title_tag.get_text(strip=True)
            link_org = title_tag["href"]

            # 언론사 추출
            source_tag = article.find("a", class_="info press")
            newspaper_org = source_tag.get_text(strip=True).replace("언론사 선정", "").strip() if source_tag else ""

            # 설정 파일(news_parsing_config.json)에 포함된 언론사만 처리하는 로직
            site_config = get_site_config(newspaper_org)
            if site_config is None:
                logging.info(f"설정 파일에 없는 언론사 기사 스킵: {newspaper_org}")
                continue

            # 작성일 추출(날짜 형식, 상대 시간 여부 확인)
            date_str = article.find("span", class_="info").get_text(strip=True)
            pub_date_org = parse_date(date_str)

            # 날짜 변환 실패 시 해당 기사 스킵
            if pub_date_org is None:
                logging.info(f"날짜 변환 실패로 기사 스킵: {title_org}")
                continue

            if pub_date_org and pub_date_org < base_date:
                logging.info(f"기준 날짜 이전 기사 감지. 크롤링 중단.")
                continue

            # 1단계: 기사 기본 정보 저장(본문 미수집)
            save_news_db(title_org, newspaper_org, pub_date_org.strftime("%Y-%m-%d %H:%M:%S"), None, link_org)

            # 2단계: 기사 본문(content_org)을 즉시 크롤링하여 DB 업데이트
            content_org = extract_article_text(link_org)
            if content_org and len(content_org) > 50:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE news_data SET content_org = %s WHERE link_org = %s", (content_org, link_org))
                    conn.commit()
                    conn.close()
                    logging.info(f"본문 저장 완료: {title_org}")
                except Exception as e:
                    logging.error(f"본문 저장 오류: {e}")

        page += 1
        time.sleep(random.uniform(10, 15))


# [ 실행 ]
if __name__ == "__main__":
    fetch_naver_news()