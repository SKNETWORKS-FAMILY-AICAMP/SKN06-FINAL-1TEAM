from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
import os, json, re,requests,pymysql,joblib
from rapidfuzz import process, fuzz
import pandas as pd
from main.question.title_mapping import find_best_matching_titles
from main.question.company_extraction import extract_company_and_info, get_candidate_companies, get_valid_company

def summarize_content(content: str, question: str,llm) -> str:
    """
    검색된 문서 내용을 질문에 맞게 요약하여 반환
    """
    summary_prompt = f"""
        사용자의 질문: "{question}"

        당신은 사업보고서를 분석하여 필요한 데이터를 정확히 제공하는 전략팀입니다.
        사용자의 질문과 관련된 데이터가 테이블 형태로 제공된다면, **반드시 테이블에서 먼저 데이터를 추출**하세요.

        💡 **답변 방식**
        1. 질문이 "최근 3년간 매출, 영업이익, 당기순이익"과 같은 정량적 데이터 요청이라면:
        - 테이블에서 해당 데이터를 찾고, 표 형태 그대로 제공하세요.
        - 만약 테이블이 없다면 본문에서 해당 수치를 찾아 제공합니다.

        2. 질문이 "별도재무제표" 기준인지 "연결재무제표" 기준인지 확인하고, 맞는 데이터를 선택하세요.

        3. 필요 없는 설명 없이 **정확한 수치 데이터만 출력**하세요.

        📑 **검색된 문서 내용**:
        {content}

        위 내용을 참고하여, 사용자의 질문에 간결하고 정확한 답변을 생성하세요.
        """

    summary = llm.invoke(summary_prompt).content.strip()
    return summary

def aggregate_results(valid_results: list, query: str, company: str,llm) -> str:
    """
    여러 문서에서 추출된 해당 기업 관련 데이터를 전략팀 관점에서 분석하여,
    해당 기업의 '{query}'이(가) 기업 경쟁력 및 시장 내 위치에 미치는 영향과
    향후 전략 수립에 대한 시사점을 종합하는 최종 보고서를 작성합니다.
    
    --- 시작 ---
    {combined_content}
    --- 끝 ---
    """
    combined_content = "\n".join(valid_results)
    final_prompt = f"""
        ### 📌 {company}의 {query} 관련 정보 검색 결과

        아래는 {company}의 사업보고서에서 추출한 {query} 관련 데이터입니다.  
        문서에서 제공된 데이터를 기반으로 **가장 관련성이 높은 정보**를 제공합니다.  
        📌 **주의:** 불필요한 설명 없이 **정확한 원본 데이터**와 **핵심 분석 정보**를 구분하여 제공하세요.
        **요구사항:**
        - 중요한 내용 외 부가적인 내용은 생략할 것.
        - 표 데이터는 해석 후 반드시 줄 글 형식으로 하여 제공할 것.
        - 답변은 150자 이내의 간결한 문장으로 작성할 것.
        - 질문에 대한 답변을 반드시 포함할 것.
        - 반드시 정확한 값을 기반으로 답변을 작성할 것.
        - 최종 결과는 반드시 줄 글(plain text) 형식이어야 함.
        - 존댓말 형식으로 답변을 출력해야 함.
        - 금액 관련 정보가 있을 경우, 해당 정보의 시점(연도, 일자 등)을 반드시 명시할 것.


        ---
        ### **1️⃣ 원본 데이터 (검색된 문서 내용)**
        📄 **출처: 사업보고서**
    --- 시작 ---
    {combined_content}
    --- 끝 ---
    """
    final_summary = llm.invoke(final_prompt).content.strip()
    return final_summary


def process_question_query(query: str, collection, llm):
    """
    사용자의 질문을 처리하여 최적의 기업 정보를 찾아 제공하는 함수.
    """
    company_names, info = extract_company_and_info(query, llm)
    if not company_names or not info:
        return "❌ 질문에서 필요한 정보를 정확히 추출하지 못했습니다."
    
    responses = ""

    for company in company_names:
        # ✅ 올바른 기업명을 결정
        valid_company = get_valid_company(company, collection, llm)
        
        # ✅ 회사의 타이틀 목록 검색
        results = collection.get(where={"company": valid_company}, include=["metadatas"])
        if not results["metadatas"]:
            responses += f"❌ {valid_company}의 사업보고서 데이터를 찾을 수 없습니다.\n"
            continue

        company_titles = list(set([doc["title"] for doc in results["metadatas"] if "title" in doc]))
        
        # ✅ 가장 적절한 title 선택
        best_titles = find_best_matching_titles(info, llm, company_titles, top_k=3)
        if not best_titles:
            responses += f"❌ {valid_company}의 적절한 데이터를 찾을 수 없습니다.\n"
            continue
        
        valid_results = []
        for title in best_titles:
            # ✅ 해당 title 관련 데이터 검색
            results = collection.similarity_search(
                f"{title}",
                filter={"$and": [{"company": valid_company}, {"title": title}]},
                k=1
            )

            if results:
                for doc in results:
                    source = doc.metadata.get("source", "출처정보 없음")
                    summary = summarize_content(doc.page_content, query, llm)
                    if "관련 정보를 찾을 수 없습니다" not in summary:
                        valid_results.append(f"\n📄 출처: {source}\n{summary}\n")
                        break
        
        # ✅ 최종 응답 생성
        if valid_results:
            aggregated_result = aggregate_results(valid_results, info, valid_company, llm)
            responses += aggregated_result
        else:
            responses += f"❌ {valid_company}의 {info} 정보를 찾을 수 없습니다.\n"

    return responses



def process_question_query(query: str, collection, llm):
    print("함수")
    """
    사용자의 질문을 단계별로 처리하여 최적의 기업 정보(title)를 찾아 제공하는 함수.
    """
    company_names, info = extract_company_and_info(query, llm)
    if not company_names or not info:
        return "❌ 질문에서 필요한 정보를 정확히 추출하지 못했습니다."
    
    responses = ""
    for company in company_names:
        # 올바른 기업명을 결정 (DB에 없으면 후보 목록을 보여주고 사용자에게 입력받음)
        valid_company = get_valid_company(company, collection,llm)
        if "유사한 기업 목록" in valid_company:
            return f"❌ {valid_company}\n기업명을 정확히 입력해주세요."
        print(f"\n🔎 [STEP 2] {valid_company}의 title 목록 검색 중...")
        results = collection.get(
            where={"company": valid_company},
            include=["metadatas"],
        )
        if not results["metadatas"]:
            responses += f"❌ {valid_company}의 사업보고서 데이터를 찾을 수 없습니다.\n"
            print(f"🚨 {valid_company}의 title 목록을 찾을 수 없음")
            continue
        company_titles = list(set([doc["title"] for doc in results["metadatas"] if "title" in doc]))
        print(f"📌 [STEP 2 결과] {valid_company}의 title 목록: {company_titles}")
        
        best_titles = find_best_matching_titles(info,llm, company_titles, top_k=3)
        if not best_titles:
            responses += f"❌ {valid_company}의 적절한 데이터를 찾을 수 없습니다.\n"
            continue
        print(f"📌 [STEP 3 결과] 선택된 title (우선순위): {best_titles}")
        
        valid_results = []
        for title in best_titles:
            print(f"\n🔎 [STEP 4] {valid_company} - '{title}' 데이터 검색 중...")
            results = collection.similarity_search(
    f"{title}",
    filter={"$and": [{"company": valid_company}, {"title": title}]},
    k=1
)
            if results:
                for doc in results:
                    source = doc.metadata.get("source", "출처정보 없음")
                    summary = summarize_content(doc.page_content, query,llm)
                    if "관련 정보를 찾을 수 없습니다" not in summary:
                        valid_results.append(f"\n📄 출처: {source}\n{summary}\n")
                        break
        if valid_results:
            aggregated_result = aggregate_results(valid_results, info, valid_company, llm)
            responses += aggregated_result
        else:
            responses += f"❌ {valid_company}의 {info} 정보를 찾을 수 없습니다.\n"
    return responses