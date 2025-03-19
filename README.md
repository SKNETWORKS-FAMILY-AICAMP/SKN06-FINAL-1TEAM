# SKN06-FINAL-1TEAM
박창규, 백하은, 성은진, 김지영, 노원재
# 프로젝트: AI 기반 기업 분석 시스템
<table>
  <tr>
    <th>창규</th>
    <th>지영</th>
    <th>원재</th>
    <th>하은</th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/de728c8a-6828-4cc8-b057-b104815c7d07" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/7535cfb6-83f2-4c1c-ad20-3714a590e6ee" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/e138400d-7b88-4e12-884e-6f8c86f48424" width="200"></td>
    <td><img src="https://github.com/user-attachments/assets/d120b931-2ef6-41b6-8b16-0b747bdcae1e" width="200"></td>
  </tr>
</table>





## 🛠 Teach Stack

<table>
  <tr>
    <th>Front-end</th>
    <th>Back-end</th>
    <th>AI & LLMs</th>
    <th>DevOps & Cloud</th>
  </tr>
  <tr>
    <td>
      <img src="https://img.shields.io/badge/CSS-1572B6?style=flat&logo=css3&logoColor=white">
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black">
    </td>
    <td>
      <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white">
      <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white">
      <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white">
    </td>
    <td>
      <img src="https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white">
      <img src="https://img.shields.io/badge/Gemini-4285F4?style=flat&logo=google&logoColor=white">
      <img src="https://img.shields.io/badge/LangChain-black?style=flat&logo=python&logoColor=white">
      <img src="https://img.shields.io/badge/HuggingFace-yellow?style=flat&logo=huggingface&logoColor=white">
    </td>
    <td>
      <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white">
      <img src="https://img.shields.io/badge/AWS-orange?style=flat&logo=amazon-aws&logoColor=white">
    </td>
  </tr>
</table>




## 개요
본 프로젝트는 기업 전략팀을 위한 AI 기반 기업 분석 및 데이터 요약 시스템입니다.
사용자가 기업명, 재무정보, 산업 동향, 리스크 평가 등 다양한 질의를 입력하면, 최적의 데이터를 검색 및 분석하여 인사이트를 제공하는 RAG(Retrieval-Augmented Generation) 기반 AI 시스템을 구축하였습니다.

## 주요 기능
- ✅ AI 기반 검색 및 요약: LLM과 다중 에이전트 시스템을 활용하여 기업 데이터를 신속하게 분석
- ✅ 재무 정보 및 리스크 평가: 기업의 주요 재무 지표, 위험 요인 등을 한눈에 파악 가능
- ✅ 최신 뉴스 모니터링: 실시간 크롤링을 통해 기업 관련 최신 뉴스 및 트렌드 제공
- ✅ 데이터 시각화: 재무 분석 및 시장 동향을 직관적인 그래프 및 차트로 표현

이 모든 기능을 웹 기반 인터페이스를 통해 쉽게 사용할 수 있도록 구현하였습니다.
## 시스템 아키텍처

![시스템구성도](https://github.com/user-attachments/assets/5ce35c69-aa8c-4365-a5a2-da4061d81e00)

- **백엔드**: Django 템플릿 기반 서버 사이드 렌더링 (SSR) 
- **데이터 저장**: MySQL (구조화 데이터), ChromaDB (벡터 데이터)
- **AI 모델**: OpenAI GPT, BERT 기반 NLP 모델
- **클라우드 인프라**: AWS EC2, Docker 컨테이너 기반 배포
- **데이터 수집**: OpenDART API, Selenium 웹 크롤러

## 데이터 처리 흐름
1. **데이터 수집**
   - OpenDART API: 기업 재무제표, 기업 개황, 임직원 현황, 사업보고서 수집
   - 웹 크롤링: 네이버 뉴스 크롤링 (Selenium, BeautifulSoup 활용)
   - 데이터 저장: MySQL 및 ChromaDB 활용

2. **데이터 전처리**
   - **사업보고서 변환 및 벡터화**  
     - PDF 기반 사업보고서를 Markdown 형식으로 변환 `(PyMuPDF4LLM)`
     - 목차를 `###` 기준으로 구조화하여 가독성 향상  
     - `MarkDownTextSplitter`를 활용한 문서 단위 분할 및 벡터 임베딩 (ChromaDB 저장)  
   - **재무 데이터 정규화**  
     - 날짜 데이터 정규화 (YYYY-MM-DD 형식 통일)  
     - 사용하지 않는 컬럼 제거 및 데이터 정리  
   - **뉴스 데이터 분석**  
     - 키워드 추출 및 감성 분석 (BERT 모델 활용)  

3. **AI 분석 및 검색**
   - **검색 Agent**: 벡터 검색을 통해 기업별 데이터 검색
   - **요약 Agent**: GPT 기반 문서 요약 및 질의응답
   - **예측 Agent**: 머신러닝 기반 매출 예측
   - **뉴스 Agent**: 뉴스 감성 분석 및 트렌드 탐색

4. **결과 제공**
   - Django 템플릿을 활용한 동적 웹 페이지 렌더링  
   - 질의응답(Q&A) 기능을 통한 기업 분석 및 예측 결과 제공  
   - 데이터 시각화를 포함한 대시보드 제공  
     

## 모델 성능 평가
- **검색 모델 Precision@5**: 82%
- **NLP 모델 BLEU Score**: 89.5
- **예측 모델 R² Score**: 0.95

## 향후 개선 방향
1. **예측 모델 고도화**
   - LSTM 기반 시계열 분석 모델 도입
   - 뉴스 감성 분석 결과를 예측 모델에 반영

2. **데이터 전처리**
   - 사업보고서 내 다양한 형식의 데이터를 정규화하여 일관된 구조로 변환
     
3. **검색 및 요약 최적화**
   - ChromaDB 벡터 검색 성능 개선
   - 도메인 지식을 활용한 사용자 질문에 대한 mapping 도입

## 프로젝트 팀
- **백하은**: 데이터 전처리 및 AI 모델 개발
- **김지영**: 데이터 수집 및 데이터베이스 관리
- **노원재**: 시스템 아키텍처 설계
- **박창규**: 모델 평가 및 테스트 계획 수립

## 깃허브 저장소
🔗 [프로젝트 깃허브](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN06-FINAL-1TEAM)

## 라이선스
본 프로젝트는 MIT 라이선스를 따릅니다.


## 회고
- **백하은**: 
- **김지영**: 
- **노원재**: "우리가 쌓아온 코드와 고민의 흔적들은 사라지지 않는다. 그것들은 우리가 함께 만든 하나의 길이 되어, 다음 도전을 향한 나침반이 될 것이다."
- **박창규**:
- **성은진**: 날먹 개꿀 ㅋㅋ

