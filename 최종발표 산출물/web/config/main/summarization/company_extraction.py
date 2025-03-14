import json,re
def extract_company_and_info(query: str, llm):
    """
    질문에서 기업명과 필요한 정보를 JSON 형태로 추출
    """
    print(f"\n🔎 [STEP 1] 기업명 추출 중...")
    extraction_prompt = f"""
    사용자의 질문에서 기업명과 필요한 정보를 JSON 형식으로 추출하세요.
    질문: "{query}"
    
    반드시 아래 형식으로만 출력하세요:
    {{"기업명": ["기업명1", "기업명2"], "정보": "전체 질문"}}
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

def get_candidate_companies(extracted_company: str, collection, llm) -> list:
    """
    DB에 저장된 전체 기업명 목록 중, 사용자가 입력한 기업명과 유사한 기업들을 GPT를 통해 반환합니다.
    출력은 쉼표로 구분된 기업명 문자열을 리스트로 반환합니다.
    """
    all_docs = collection.get(include=["metadatas"])
    print("all_docs :", all_docs)
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

def get_valid_company(extracted_company: str, collection,llm) -> str:
    """
    추출된 기업명을 그대로 DB에서 검색하여 데이터가 있으면 그대로 사용하고,
    없으면 후보 목록을 보여주어 사용자에게 올바른 기업명을 직접 입력받도록 합니다.
    """
    results = collection.get(where={"company": extracted_company}, include=["metadatas"])
    if results["metadatas"]:
        return extracted_company
    else:
        candidates = get_candidate_companies(extracted_company, collection, llm)

        return f"입력하신 '{extracted_company}'와 유사한 기업 목록: {', '.join(candidates)}"