#####################################################
# MySQL 연결 객체 반환 함수, 네트워크 요청 재시도 모듈
#####################################################

import time
import requests
import pymysql
import logging

DB_CONFIG = {
    "host": "3.34.124.117",
    "user": "stratify",
    "password": "1111",
    "database": "stratify",
    "port": 3306,
    "charset": "utf8mb4"
}

def get_db_connection():
    """
    MySQL 연결 객체를 반환하는 함수
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.MySQLError as e:
        logging.error(f"데이터베이스 연결 실패: {e}")
        return None
    

def safe_request(url, headers, params=None, max_retries=3, timeout=10):
    """
    네트워크 요청을 안전하게 수행하는 함수 - 재시도 기법(Exponential Backoff)
    - 요청 실패 시 최대 max_retries만큼 재시도
    - 추가적인 요청 파라미터(params) 허용
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()  # HTTP 오류가 있으면 예외 발생
            return response
        except requests.RequestException as e:
            logging.warning(f"요청 실패 {attempt + 1}/{max_retries}회: {e}")
            time.sleep(2 ** attempt)  # 점진적으로 대기 시간 증가 (exponential backoff)
    
    logging.error(f"최대 재시도 횟수 초과: {url}")
    return None  # 요청 실패 시 None 반환