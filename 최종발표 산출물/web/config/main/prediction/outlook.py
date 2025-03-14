def determine_outlook(operating_margin, debt_ratio, sales_growth_rate, liquidity_ratio):
    """
    영업이익률, 부채비율, 매출액 증가율, 유동비율을 기반으로 기업 전망을 결정
    """

    # 긍정적 기준 (🟢)
    positive_criteria = [
        operating_margin >= 5,  # 영업이익률 5% 이상
        debt_ratio <= 100,      # 부채비율 100% 이하
        sales_growth_rate >= 5, # 매출 성장률 5% 이상
        liquidity_ratio >= 120  # 유동비율 120% 이상
    ]
    
    # 부정적 기준 (🔴)
    negative_criteria = [
        operating_margin < 3,   # 영업이익률 3% 미만
        debt_ratio >= 200,      # 부채비율 200% 이상
        sales_growth_rate < 0,  # 매출 감소
        liquidity_ratio < 80    # 유동비율 80% 미만
    ]

    # 긍정적 전망 (3개 이상 충족)
    if sum(positive_criteria) >= 3:
        return "🟢 긍정"

    # 부정적 전망 (3개 이상 충족)
    elif sum(negative_criteria) >= 3:
        return "🔴 부정"

    # 그 외 불투명 (중립적) 전망
    else:
        return "🟡 불투명"