# SKN06-FINAL-1TEAM
박창규, 백하은, 성은진, 김지영, 노원재
# 프로젝트: AI 기반 기업 분석 시스템

## 개요
본 프로젝트는 기업 분석 및 투자 전략 수립을 지원하는 **AI 기반 검색 및 데이터 요약 시스템**입니다. 사용자가 기업 관련 질의를 하면, 최적의 데이터를 검색 및 분석하여 유용한 인사이트를 제공하는 **다중 에이전트 기반 RAG(Retrieval-Augmented Generation) 시스템**을 구축하였습니다.

## 주요 기능
- **사업 보고서 요약**: OpenAI GPT 기반 요약 및 검색 기능 제공
- **기업 재무 데이터 분석**: OpenDART API를 통해 수집한 재무제표 데이터를 분석하여 기업 전망 예측
- **실시간 뉴스 분석**: 크롤링을 통한 실시간 뉴스 수집 및 감성 분석 수행
- **AI 기반 검색**: Chroma DB를 활용한 벡터 검색 및 질의응답(Q&A) 기능 지원
- **예측 모델링**: 머신러닝(선형 회귀, 다중 회귀) 기반 재무 예측

## 시스템 아키텍처
![시스템 아키텍처](시스템구성도.png)

- **백엔드**: Django 기반 REST API 구축
- **데이터 저장**: MySQL (구조화 데이터), ChromaDB (벡터 데이터)
- **AI 모델**: OpenAI GPT, BERT 기반 NLP 모델
- **클라우드 인프라**: AWS EC2, Docker 컨테이너 기반 배포
- **데이터 수집**: OpenDART API, Selenium 웹 크롤러

## 데이터 처리 흐름
1. **데이터 수집**
   - OpenDART API: 기업 재무제표 수집
   - 웹 크롤링: 네이버 뉴스 크롤링 (Selenium, BeautifulSoup 활용)
   - 데이터 저장: MySQL 및 ChromaDB 활용

2. **데이터 전처리**
   - 텍스트 정제 및 벡터화 (ChromaDB 임베딩)
   - 재무 데이터 단위 변환 및 정규화
   - 뉴스 데이터 감성 분석 및 키워드 추출 (BERT 모델 사용)

3. **AI 분석 및 검색**
   - **검색 Agent**: 벡터 검색을 통해 기업별 데이터 검색
   - **요약 Agent**: GPT 기반 문서 요약 및 질의응답
   - **예측 Agent**: 머신러닝 기반 매출 예측
   - **뉴스 Agent**: 뉴스 감성 분석 및 트렌드 탐색

4. **결과 제공**
   - API를 통해 프론트엔드 또는 외부 시스템에 응답 반환
   - 질의응답(Q&A) 기능을 통한 기업 분석 및 예측 결과 제공

## 설치 및 실행 방법
### 1. 필수 요구 사항
- Python 3.8 이상
- Django, MySQL, ChromaDB
- Docker 및 AWS EC2 환경 (선택 사항)

### 2. 프로젝트 클론 및 환경 설정
```bash
git clone https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN06-FINAL-1TEAM.git
cd SKN06-FINAL-1TEAM
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### 3. 데이터베이스 설정
```bash
# MySQL DB 생성
CREATE DATABASE ai_project;

# 환경 변수 설정 (.env 파일 생성)
DATABASE_URL=mysql://user:password@localhost/ai_project
```

### 4. 서버 실행
```bash
python manage.py migrate
python manage.py runserver
```

## API 사용 방법
### 1. 사업 보고서 검색 API
- **Endpoint**: `/api/search`
- **Method**: POST
- **Request Body**:
```json
{
  "query": "현대자동차 2024년 사업 보고서"
}
```
- **Response**:
```json
{
  "summary": "현대자동차의 2024년 매출은 100조 원으로, 전년 대비 10% 증가했습니다.",
  "keywords": ["매출", "자동차 산업", "전기차"]
}
```

### 2. 재무 예측 API
- **Endpoint**: `/api/predict`
- **Method**: POST
- **Request Body**:
```json
{
  "company": "현대자동차",
  "year": 2025
}
```
- **Response**:
```json
{
  "predicted_revenue": "110조 원",
  "confidence": "95%"
}
```

## 모델 성능 평가
- **검색 모델 Precision@5**: 82%
- **NLP 모델 BLEU Score**: 89.5
- **예측 모델 R² Score**: 0.95

## 향후 개선 방향
1. **예측 모델 고도화**
   - 다중 회귀 및 LSTM 기반 시계열 분석 모델 도입
   - 뉴스 감성 분석 결과를 예측 모델에 반영

2. **검색 및 요약 최적화**
   - ChromaDB 벡터 검색 성능 개선
   - GPT 프롬프트 엔지니어링을 통한 응답 품질 향상

3. **API 성능 최적화**
   - Django API의 속도 및 응답 성능 개선
   - 대량 데이터 처리 최적화

## 프로젝트 팀
- **백하은**: 데이터 전처리 및 AI 모델 개발
- **김지영**: 데이터 수집 및 데이터베이스 관리
- **노원재**: 시스템 아키텍처 설계
- **박창규**: 모델 평가 및 테스트 계획 수립

## 깃허브 저장소
🔗 [프로젝트 깃허브](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN06-FINAL-1TEAM)

## 라이선스
본 프로젝트는 MIT 라이선스를 따릅니다.

