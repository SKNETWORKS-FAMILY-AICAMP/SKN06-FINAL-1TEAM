from dotenv import load_dotenv
import os, json, re
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

embedding_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=api_key)

# Chroma 및 embedding_model 관련 모듈/객체를 미리 임포트 및 초기화했다고 가정합니다.
collection = Chroma(
    collection_name="company_docs",
    embedding_function=embedding_model,
    persist_directory="./chromadb_store"
)

# LLM 모델 초기화 (전략팀용 분석에도 활용)
llm = ChatOpenAI(model_name="gpt-4o-mini")

def extract_company_and_info(query: str):
    """
    질문에서 기업명과 필요한 정보를 JSON 형태로 추출
    """
    print(f"\n🔎 [STEP 1] 기업명 추출 중...")
    extraction_prompt = f"""
    사용자의 질문에서 기업명과 필요한 정보를 JSON 형식으로 추출하세요.
    질문: "{query}"
    
    반드시 아래 형식으로만 출력하세요:
    {{"기업명": ["기업명1", "기업명2"], "정보": "질문에서 필요한 정보"}}
    """
    extraction_result = llm.invoke(extraction_prompt).content.strip()
    extraction_result = re.sub(r"```json|```", "", extraction_result).strip()
    print(f"📌 [STEP 1 결과] 기업명 & 정보 추출 (정리 후): {extraction_result}")
    try:
        extracted_data = json.loads(extraction_result)
        company_names = extracted_data.get("기업명", [])
        info = extracted_data.get("정보", "").strip()
    except json.JSONDecodeError:
        print("🚨 JSON 파싱 오류 발생. GPT의 응답을 확인하세요.")
        return None, None
    if not company_names or not info:
        print("🚨 기업명 또는 정보가 부족함.")
        return None, None
    return company_names, info

def get_candidate_companies(extracted_company: str) -> list:
    """
    DB에 저장된 전체 기업명 목록 중, 사용자가 입력한 기업명과 유사한 기업들을 GPT를 통해 반환합니다.
    출력은 쉼표로 구분된 기업명 문자열을 리스트로 반환합니다.
    """
    all_docs = collection.get(include=["metadatas"])
    company_set = set()
    for doc in all_docs["metadatas"]:
        if "company" in doc:
            company_set.add(doc["company"])
    company_list = list(company_set)
    if not company_list:
        return []
    company_list_str = ", ".join(company_list)
    prompt = f"""
    사용자가 입력한 기업명: "{extracted_company}".
    DB에 저장된 기업명 목록: [{company_list_str}].
    위 목록 중, 사용자가 입력한 기업명과 유사한 기업들을 모두 출력해 주세요.
    출력은 오직 기업명만 쉼표로 구분하여 하나의 문자열로 출력해 주세요.
    """
    response = llm.invoke(prompt).content.strip()
    candidates = [x.strip() for x in response.split(",") if x.strip()]
    return candidates

def get_valid_company(extracted_company: str) -> str:
    """
    추출된 기업명을 그대로 DB에서 검색하여 데이터가 있으면 그대로 사용하고,
    없으면 후보 목록을 보여주어 사용자에게 올바른 기업명을 직접 입력받도록 합니다.
    """
    results = collection.get(where={"company": extracted_company}, include=["metadatas"])
    if results["metadatas"]:
        return extracted_company
    else:
        candidates = get_candidate_companies(extracted_company)
        if candidates:
            print(f"입력하신 '{extracted_company}'와 유사한 기업 목록: {', '.join(candidates)}")
            new_company = input("올바른 기업명을 입력해주세요: ").strip()
            return new_company
        else:
            return extracted_company

def find_best_matching_titles(query: str, available_titles: list, top_k: int = 3) -> list:
    """
    사용자의 질문과 가장 유사한 title을 최대 top_k개까지 반환
    """
    selection_prompt = f"""
    사용자의 질문에서 필요한 정보를 찾을 수 있는 가장 적절한 'title'을 아래 목록에서 최대 {top_k}개 선택하세요.
    
    질문: "{query}"
    사용 가능한 title 목록: {available_titles}
    
    가장 관련 있는 title을 ','로 구분하여 하나의 문자열로 출력하세요. 없는 경우 "없음"을 반환하세요.
    """
    selected_titles = llm.invoke(selection_prompt).content.strip()
    if selected_titles == "없음":
        return []
    return [title.strip() for title in selected_titles.split(",") if title.strip()]

def summarize_content(content: str, question: str) -> str:
    """
    검색된 문서 내용을 질문에 맞게 요약하여 반환
    """
    summary_prompt = f"""
    사용자의 질문: "{question}"
    
    "너는 사업보고서 데이터를 기반으로 질문에 대해 정확한 답변을 제공하는 AI야.
    표 데이터와 텍스트 데이터를 모두 검색하여 가장 관련 있는 정보를 바탕으로 응답해야 해.
    반드시 사업보고서 내의 정보를 바탕으로 대답해야 하며, 임의의 추론이나 가정은 허용되지 않아.
    답변은 300자 이내, 3문장 이내로 간결하게 정리해야 해.
    
    ### ✅ 답변 생성 규칙
    1. 표 데이터 분석: 질문에 해당하는 표 데이터를 찾고, 숫자를 정확히 읽어야 함.
    2. 텍스트 데이터 검색: 질문과 가장 관련 있는 텍스트 내용을 참고하여 정확한 답변을 제공.
    3. 연도 매칭: '제55기' 같은 표현을 실제 연도로 변환하여 올바른 데이터를 제공해야 함.
    4. 숫자 포맷 변환: 35,629,100,000 같은 수치는 35조 6,291억 원 형태로 변환하여 가독성을 높임.
    5. 출처 명확히 표시: 사용된 데이터의 출처(사업보고서 파일명, TITLE)를 답변에 포함해야 함.
    6. 불확실한 정보 배제: 질문과 직접적으로 일치하는 정보가 없다면, 유사한 내용을 제공하되 확실한 사실만 포함해야 함.
    
    ### ✅ 추가 질문 규칙 (정보 부족 시 재질문)
    - 회사명이 없는 경우: "어떤 회사의 정보를 찾으시나요?"
    - 연도 정보가 없는 경우: "어느 연도의 정보를 찾으시나요?"
    - 질문이 불명확한 경우: "질문이 모호합니다. 어떤 정보를 원하시는지 좀 더 구체적으로 말씀해 주세요."
    - 찾을 수 있는 데이터가 없을 경우: "관련 정보를 찾을 수 없습니다. 다른 질문을 해주시겠어요?"
    
    관련된 사업보고서 내용:
    {content}
    
    사용자의 질문에 대해 간결하고 정확한 답변을 만들어 주세요.
    """
    summary = llm.invoke(summary_prompt).content.strip()
    return summary

def aggregate_results(valid_results: list, query: str, company: str) -> str:
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
    다음은 여러 사업보고서 문서에서 추출된 {company} 관련 데이터입니다.
    전략팀의 관점에서, 위 데이터를 바탕으로 {company}의 {query}이(가)
    기업 경쟁력 및 시장 내 위치에 미치는 영향과 향후 전략적 대응 방안을 평가하는 보고서를 작성해 주세요.
    각 데이터의 출처를 간략히 언급하고, 답변은 300자 이내, 3문장 이내로 작성해 주세요.
    
    --- 시작 ---
    {combined_content}
    --- 끝 ---
    """
    final_summary = llm.invoke(final_prompt).content.strip()
    return final_summary

def process_question(query: str) -> str:
    """
    사용자의 질문을 단계별로 처리하여 최적의 기업 정보(title)를 찾아 제공하는 함수.
    """
    company_names, info = extract_company_and_info(query)
    if not company_names or not info:
        return "❌ 질문에서 필요한 정보를 정확히 추출하지 못했습니다."
    
    responses = ""
    for company in company_names:
        # 올바른 기업명을 결정 (DB에 없으면 후보 목록을 보여주고 사용자에게 입력받음)
        valid_company = get_valid_company(company)
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
        
        best_titles = find_best_matching_titles(info, company_titles, top_k=3)
        if not best_titles:
            responses += f"❌ {valid_company}의 적절한 데이터를 찾을 수 없습니다.\n"
            continue
        print(f"📌 [STEP 3 결과] 선택된 title (우선순위): {best_titles}")
        
        valid_results = []
        for title in best_titles:
            print(f"\n🔎 [STEP 4] {valid_company} - '{title}' 데이터 검색 중...")
            results = collection.similarity_search(
                f"{title}",
                filter={"company": valid_company},
                k=1
            )
            if results:
                for doc in results:
                    source = doc.metadata.get("source", "출처정보 없음")
                    summary = summarize_content(doc.page_content, query)
                    if "관련 정보를 찾을 수 없습니다" not in summary:
                        valid_results.append(f"\n📄 출처: {source}\n{summary}\n")
                        break
        if valid_results:
            aggregated_result = aggregate_results(valid_results, info, valid_company)
            responses += aggregated_result
        else:
            responses += f"❌ {valid_company}의 {info} 정보를 찾을 수 없습니다.\n"
    return responses

# 사용 예시
user_question = "현대자동차 당기이익 알려줘"
response = process_question(user_question)
print(response)
