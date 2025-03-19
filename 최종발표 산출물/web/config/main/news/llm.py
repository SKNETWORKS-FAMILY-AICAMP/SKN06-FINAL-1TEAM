from main.news.database import get_news_content
from main.news.keyword_extraction import extract_keyword
import json

def search_news_by_keywords(news_data, keywords):
    """
    가져온 뉴스 데이터에서 키워드가 포함된 기사만 필터링
    """
    filtered_news = []
    for news in news_data:
        content = news.get("content_display", "")
        if any(keyword in content for keyword in keywords):
            filtered_news.append(news)

    return filtered_news[:10]

def summarize_news(candidate_news, query, llm):
    """
    뉴스 기사 전체를 분석하여 최근 자동차 산업의 언론 동향을 요약하고, 기사 링크를 반환
    """
    if not candidate_news:
        return "**❌ 관련 뉴스가 없습니다.**", ["❌ 관련 기사 없음"]

    print("news:", candidate_news[:2])

    valid_news_texts = []
    for news in candidate_news:
        summary_text = news.get("summary")  # ✅ "summary"가 있는 경우 사용
        content_text = news.get("content_display", "내용 없음")  # ✅ "content_display"를 기본값으로 사용
        valid_news_texts.append(summary_text if summary_text else content_text)  # ✅ summary가 없으면 content 사용

    # 뉴스 본문을 하나의 텍스트로 결합
    combined_text = "\n\n".join(valid_news_texts)

    # 🆕 고정된 답변 형식 유지하는 프롬프트
    summary_prompt = f"""
    사용자의 질문: "{query}"

    아래는 최근 자동차 산업에 대한 뉴스 기사입니다. 
    이 뉴스를 기반으로 자동차 산업의 최신 트렌드를 분석해 주세요.

    🔹 트렌드 분석 기준:
    1. 주요 이슈 (중요한 정책 변화, 기업 동향, 기술 혁신, 경제적 영향 등)
    2. 자주 언급되는 키워드 및 공통된 주제
    3. 긍정적인 변화 vs 부정적인 논란
    4. 앞으로의 전망 (업계 전문가나 언론이 어떻게 예측하는지)

    🚗 **답변은 아래의 형식으로 작성해 주세요:**  

    ```
    📰 최근 자동차 산업의 언론 동향: 최근 자동차 산업의 언론 동향은 다음과 같습니다.

    주요 이슈:  
    - (여기에 최근 주요 이슈 내용)

    자주 언급되는 키워드:  
    - (관련 키워드 나열)

    긍정적인 변화 vs 부정적인 논란:  
    - (긍정적인 평가 vs 논란 요소)

    앞으로의 전망:  
    - (전망 및 예측)

    이러한 동향은 시장의 불확실성을 높이며, 기업들이 적응해야 할 새로운 환경을 만들어가고 있습니다.
    ```

    {combined_text}
    """

    summary = llm.invoke(summary_prompt).content.strip()

    # 기사 링크 추출
    news_links = [
        news.get("link_org", "❌ 관련 기사 없음")
        for news in candidate_news if news.get("link_org")
    ]

    return summary, news_links

def process_news_query(query, collection, llm):
    """
    사용자의 질문을 바탕으로 관련 뉴스를 찾아 자동차 산업의 언론 동향을 분석하여 반환하는 함수
    """
    print(f"뉴스 요약 요청: {query}")

    # 1️⃣ 키워드 추출
    keywords = extract_keyword(query, llm)
    print("키워드:", keywords)

    # 2️⃣ DB에서 뉴스 가져오기
    news_data = get_news_content()

    # 3️⃣ 키워드 기반 뉴스 필터링
    news_results = search_news_by_keywords(news_data, keywords)
    print("관련 뉴스 개수:", len(news_results))

    # 4️⃣ 트렌드 분석 기반 요약 (자동 생성된 요약 사용)
    combined_summary, news_links = summarize_news(news_results, query, llm)

    # 5️⃣ 최종 결과 문자열 반환 (깔끔한 마크다운 스타일 적용)
    news_links_text = "\n".join([f"- [{link}]({link})" for link in news_links]) if news_links else "관련 기사 없음"

    final_response = f"""
## 📰 최근 자동차 산업의 언론 동향

**주요 이슈**:  
   {combined_summary.split('주요 이슈:')[1].split('자주 언급되는 키워드:')[0].strip()}

**자주 언급되는 키워드**:  
   {combined_summary.split('자주 언급되는 키워드:')[1].split('긍정적인 변화 vs 부정적인 논란:')[0].strip()}

**긍정적인 변화 vs 부정적인 논란**:  
   {combined_summary.split('긍정적인 변화 vs 부정적인 논란:')[1].split('앞으로의 전망:')[0].strip()}

**앞으로의 전망**:  
   {combined_summary.split('앞으로의 전망:')[1].strip()}

🔗 **관련 기사 링크**:  
{news_links_text}
    """

    return final_response