import json

def extract_keyword(user_input, llm):
    """
    사용자의 질문에서 키워드 세가지를 추출하는 함수
    """
    extraction_prompt = f"""
    사용자의 질문에서 문맥상 키워드를 정확하게 추출하세요.
    질문: "{user_input}"
    
    형식: 
    {{
        "keyword": ["keyword1", "keyword2", "keyword3"]
    }}"""

    extraction_result = llm.invoke(extraction_prompt).content.strip()
    extracted_data = json.loads(extraction_result)

    return extracted_data.get("keyword", [])