def find_best_matching_titles(query: str,llm, available_titles: list, top_k: int = 3) -> list:
    """
    사용자의 질문과 가장 유사한 title을 최대 top_k개까지 반환
    """
    selection_prompt = f"""
    사용자의 질문에서 필요한 정보를 찾을 수 있는 가장 적절한 'title'을 아래 목록에서 최대 {top_k}개 선택하세요.
    아래 규칙을 따르세요:

    1. 질문에 "별도재무제표"가 포함되어 있다면 반드시 별도재무제표와 관련된 title만 선택하세요.
       예) "재무제표", "요약재무정보(별도)", "손익계산서(별도)" 등

    2. 질문에 "연결재무제표"가 포함되어 있다면 반드시 연결재무제표와 관련된 title만 선택하세요.
       예) "연결재무제표", "요약재무정보(연결)", "손익계산서(연결)" 등

    3. 질문이 일반적인 재무 데이터(예: "최근 3년간 매출, 영업이익, 당기순이익")를 요청하는 경우:
       - "요약재무정보" 및 "재무제표"가 포함된 title을 우선 선택하세요.

    4. "시장 점유율", "경쟁사 분석", "차별화 요소"와 관련된 질문이 포함된 경우:
       - "사업의 개요", "주요 제품 및 서비스", "매출 및 수주상황" 등의 title을 우선 선택하세요.
       - 경쟁사 관련 정보가 있는 경우, 해당 title을 포함하세요.

    5. "기타 재무에 관한 사항" 같은 title은 필요할 때만 포함하세요.

    6. 만약 질문과 정확히 일치하는 title이 없더라도, 가장 관련성이 높은 title을 선택하세요.
       (예: "시장 점유율" 질문이 있을 경우, "매출 및 수주상황"을 포함할 수 있음)

    **주의:** 반드시 가장 적절한 title 3개 이하만 선택하세요.  
    아래 형식으로 ','로 구분하여 출력하세요. 없는 경우 "없음"을 반환하세요.

    사용 가능한 title 목록: {available_titles}  
    질문: "{query}"  
    출력:
"""


    selected_titles = llm.invoke(selection_prompt).content.strip()
    if selected_titles == "없음":
        return []
    return [title.strip() for title in selected_titles.split(",") if title.strip()]


