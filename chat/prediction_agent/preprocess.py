import pandas as pd

def preprocess_financial_data(financial_data):
    """
    재무 데이터를 전처리하여 모델 입력 형식으로 변환.
    
    Args:
        financial_data (dict): IS, BS, CIS 데이터가 포함된 딕셔너리
    
    Returns:
        DataFrame: 모델이 학습한 Feature 형식으로 변환된 데이터
    """
    # 1. 데이터 병합 (3개년 데이터 포함)
    df_all = pd.concat([
        financial_data.get("is", pd.DataFrame(columns=["corp_code", "concept_id", "2023amount", "2022amount", "2021amount"])),
        financial_data.get("bs", pd.DataFrame(columns=["corp_code", "concept_id", "2023amount", "2022amount", "2021amount"])),
        financial_data.get("cis", pd.DataFrame(columns=["corp_code", "concept_id", "2023amount", "2022amount", "2021amount"]))
    ], ignore_index=True)

    # 2. 데이터 타입 변환 (숫자로 변환)
    for year in ["2023amount", "2022amount", "2021amount"]:
        df_all[year] = pd.to_numeric(df_all[year], errors="coerce")

    # 3. 데이터 Pivot 변환 (연도별로 구분)
    df_pivot = df_all.pivot_table(index="corp_code", columns="concept_id", values=["2023amount", "2022amount", "2021amount"], aggfunc="sum").reset_index()
    
    # 4. 사용할 Feature 리스트 (연도별 변수 포함)
    selected_features = [
        "ifrs-full_Assets",
        "dart_OperatingIncomeLoss",
        "ifrs-full_CurrentAssets",
        "ifrs-full_CurrentLiabilities",
        "ifrs-full_Equity",
        "ifrs-full_IssuedCapital",
        "ifrs-full_Liabilities",
        "ifrs-full_NoncurrentAssets",
        "ifrs-full_NoncurrentLiabilities",
        "ifrs-full_ProfitLoss",
        "ifrs-full_PropertyPlantAndEquipment",
        "ifrs-full_GrossProfit",
        "ifrs-full_CostOfSales"
    ]

    outlook_features = [
        "ifrs-full_Revenue", # 매출액
        "ifrs-full_Assets",
        "dart_OperatingIncomeLoss",
        "ifrs-full_CurrentAssets",
        "ifrs-full_CurrentLiabilities",
        "ifrs-full_Equity",
        "ifrs-full_IssuedCapital",
        "ifrs-full_Liabilities",
        "ifrs-full_NoncurrentAssets",
        "ifrs-full_NoncurrentLiabilities",
        "ifrs-full_ProfitLoss",
        "ifrs-full_PropertyPlantAndEquipment",
        "ifrs-full_GrossProfit",
        "ifrs-full_CostOfSales"
    ]

    # 5. 연도별 Feature 선택 (모델은 2023년 데이터 사용)

    feature_columns = ["corp_code"] + [("2023amount", feature) for feature in selected_features]
    outlook_columns = ["corp_code"] + [("2023amount", feature) for feature in outlook_features]

    # 6. Feature 선택 및 NaN 값 0으로 채우기

    outlook_df = df_pivot.reindex(columns=outlook_columns, fill_value=0)

    X_new = df_pivot.reindex(columns=feature_columns, fill_value=0)


    # 7. 컬럼명 변환 (다층 인덱스를 단일 컬럼으로 변환)
    X_new.columns = ["corp_code"] + selected_features

    outlook_df.columns = ["corp_code"] + outlook_features

    result = []

    
    result.append(X_new)
    result.append(outlook_df)

    return result
