def determine_outlook(operating_margin, debt_ratio, sales_growth_rate, liquidity_ratio):
    """
    영업이익률, 부채비율, 매출액 증가율, 유동비율을 기반으로 기업 전망을 결정
    """
    if (operating_margin >= 7 and debt_ratio <= 100 and
        sales_growth_rate >= 5 and liquidity_ratio >= 150):
        return "긍정 📈"
    elif (operating_margin <= 3 or debt_ratio >= 200 or
          sales_growth_rate <= 0 or liquidity_ratio <= 100):
        return "부정 📉"
    else:
        return "불투명 ⚖️"