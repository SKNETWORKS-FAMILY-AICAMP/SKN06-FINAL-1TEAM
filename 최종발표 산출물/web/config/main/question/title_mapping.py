def find_best_matching_titles(query: str,llm, available_titles: list, top_k: int = 3) -> list:
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


