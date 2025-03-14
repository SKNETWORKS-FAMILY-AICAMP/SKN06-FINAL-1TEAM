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
from main.summarization.title_mapping import find_best_matching_titles
from main.summarization.company_extraction import extract_company_and_info, get_valid_company

def summarize_content(content: str, question: str, llm) -> str:
    """
    검색된 문서 내용을 질문에 맞게 요약하여 반환
    """
    summary_prompt = f"""
    사용자의 질문: "{question}"

    📌 **전략팀 요약 지침**
    - 당신은 기업 보고서를 분석하는 전략팀입니다.
    - **검색된 문서에서 직접적으로 관련 있는 정보뿐만 아니라, 질문의 의미와 연결될 수 있는 정보도 포함하세요.**
    - **질문과 완전히 일치하는 정보가 없더라도, 가장 관련성이 높은 데이터를 추출하여 요약하세요.**
    - **정량적 데이터(매출, 영업이익 등)가 포함된 경우 반드시 표 형식을 유지하세요.**
    - **질문의 핵심 키워드(예: "주요 산업")와 연관된 정보를 찾아 재구성하세요.**
    - **"관련 정보를 찾을 수 없습니다"라는 답변을 절대 하지 말고, 유사한 데이터를 제공하세요.**

    📊 **데이터 처리 규칙**
    1. 질문이 재무와 관련된 질문이면 **연결재무제표**, **재무제표(단일,별도)** 중 어떤 정보를 제공 해줬는지 알려줘야 합니다.
        ex) 연결재무제표에서 찾은 재무정보인지, 재무제표(단일,별도)에서 찾은 정보인지 구분 해줘야합니다.
    
    2. 질문이 **"별도재무제표" 또는 "연결재무제표"**를 기준으로 한 요청이라면:
       - 질문에서 요구한 기준의 데이터를 제공하세요.

    3. 질문이 **"주요 산업"**과 관련된 경우:
       - **"사업의 개요", "주요 제품 및 서비스", "매출 및 수주상황"**을 종합 분석하여 현대자동차가 속한 주요 산업군을 도출하세요.
       - **단순한 사업 나열이 아니라, 현대자동차가 속한 주요 산업군(예: 자동차 제조, 모빌리티, 금융 등)을 명확히 기술하세요.**

    📑 **검색된 문서 내용**:
    --- 시작 ---
    {content}
    --- 끝 ---

    🎯 **요약된 결과**:
    """
    summary = llm.invoke(summary_prompt).content.strip()
    return summary


def aggregate_results(valid_results: list, query: str, company: str, llm) -> str:
    """
    여러 문서에서 추출된 해당 기업의 '{query}' 관련 정보를 보기 쉽게 요약하여 반환.
    """
    combined_content = "\n".join(valid_results)
    
    final_prompt = f"""
    ### 📌 {company}의 {query} 관련 사업보고서 요약

    📝 **요약 기준**
    - **질문과 완전히 일치하는 정보가 없더라도, 의미적으로 연결될 수 있는 데이터를 활용하세요. 단 일치하는 정보가 있다면 그 정보만 사용합니다**
    - **사용자 질문 의도에 맞게 핵심 내용만 반환**
    - **질문이 재무와 관련된 질문이면 **연결재무제표**, **재무제표(단일,별도)** 중 어떤 정보를 제공 해줬는지 알려줘야 합니다.
        ex) 연결재무제표에서 찾은 재무정보인지, 재무제표(단일,별도)에서 찾은 정보인지 구분 해줘야합니다.**

    📊 **1.1️⃣ 검색된 문서 분석**
    --- 시작 ---
    {combined_content}
    --- 끝 ---

    ✅ **최종 요약**
    - **분석된 내용을 토대로 간략하게 핵심 정보만 제공 **
    """
    
    final_summary = llm.invoke(final_prompt).content.strip()
    return final_summary






def process_summarization_query(query: str, collection, llm):
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
    k=5
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