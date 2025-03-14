def format_korean_currency(value):
    trillion = int(value // 1_0000_0000_0000)
    billion = int((value % 1_0000_0000_0000) // 1_0000_0000)

    if trillion > 0 and billion > 0:
        return f"{trillion}조 {billion}억"
    elif trillion > 0:
        return f"{trillion}조"
    else:
        return f"{billion}억"
    


