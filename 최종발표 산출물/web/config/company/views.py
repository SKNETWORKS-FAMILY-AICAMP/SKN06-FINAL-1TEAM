from django.shortcuts import render, get_object_or_404
from .models import CompanyList, CompanyWorker, CompanyExecutive, ConnectionBS, ConnectionCF, ConnectionCIS, ConnectionIS, SingleCIS, SingleBS, SingleCF, SingleIS
from django.core.paginator import Paginator
import json
import os
import pandas as pd
from decimal import Decimal
from django.http import JsonResponse
import joblib
from django.conf import settings
from django.db.models import Q
MODEL_PATH = os.path.join(settings.BASE_DIR, 'company', 'ml_models', 'linear_regression_model.pkl')

# 모델 로드
model = joblib.load(MODEL_PATH)


# 선택할 변수 리스트 (BS, IS, CIS 혼합)
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

health_features = selected_features + [
    "ifrs-full_retainedEarnings",
    "dart_CapitalSurplus",
    "ifrs-full_Inventories",
    "ifrs-full_FinanceCosts",
    "ifrs-full_Revenue"
]


def home_view(request):
    query = request.GET.get('q', '')  # 검색어 가져오기
    companies = CompanyList.objects.all()

    if query:
        companies = companies.filter(corp_name__icontains=query)  # 기업명 검색

    return render(request, 'home.html', {'companies': companies, 'query': query})



def company_list(request):
    # 1) 전체 기업 데이터 조회
    companies = CompanyList.objects.filter(
    Q(induty_code__startswith="30") |  # 30으로 시작하는 모든 값 포함
    Q(induty_code__startswith="301") |
    Q(induty_code__startswith="302") |
    Q(induty_code__startswith="303") |
    Q(induty_code__startswith="304")
).order_by('corp_name')
    # 2) 검색 기능 (옵션)
    search_query = request.GET.get('search', '')
    if search_query:
        # 예시: 회사명(corp_name)이나 대표자명(ceo_nm)에 검색어가 포함된 경우
        companies = companies.filter(
            corp_name__icontains=search_query
        ) | companies.filter(
            ceo_nm__icontains=search_query
        )

    # 3) 페이지네이션 (페이지당 10개씩)
    paginator = Paginator(companies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,  # 검색어를 템플릿에 전달 (입력 상자에 유지하려면)
    }
    return render(request, 'company_list.html', context)



def financial_health(request, corp_code):
    """
    기업의 재무 건전성 계산
    """
    try:
        is_data = ConnectionIS.objects.filter(corp_code=corp_code).values()
        bs_data = ConnectionBS.objects.filter(corp_code=corp_code).values()
        cis_data = ConnectionCIS.objects.filter(corp_code=corp_code).values()

        # 데이터 병합
        is_df = pd.DataFrame(list(is_data))
        bs_df = pd.DataFrame(list(bs_data))
        cis_df = pd.DataFrame(list(cis_data))
        all_data = pd.concat([is_df, bs_df, cis_df], ignore_index=True)

        # 2023년 피벗 테이블
        pivot_2023 = all_data.pivot_table(index="corp_code", columns="concept_id", values="amount_2023", aggfunc="sum").reset_index()
        pivot_2022 = all_data.pivot_table(index="corp_code", columns="concept_id", values="amount_2022", aggfunc="sum").reset_index()

        # 안전한 데이터 변환: 존재하지 않는 컬럼을 0으로 채우기
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

        health_features = selected_features + [
            "ifrs-full_retainedEarnings",
            "dart_CapitalSurplus",
            "ifrs-full_Inventories",
            "ifrs-full_FinanceCosts",
            "ifrs-full_Revenue"
        ]

        for feature in health_features:
            if feature not in pivot_2023.columns:
                pivot_2023[feature] = 0  # 필드가 없으면 기본값 0 할당
        
        for feature in health_features:
            if feature not in pivot_2022.columns:
                pivot_2022[feature] = 0

        X_2023 = pivot_2023.reindex(columns=health_features, fill_value=0)
        X_2022 = pivot_2022.reindex(columns=health_features, fill_value=0)

        # 주요 재무 비율 계산
        X_2023["current_ratio"] = (X_2023["ifrs-full_CurrentAssets"] / X_2023["ifrs-full_CurrentLiabilities"]) * 100
        X_2023["debt_ratio"] = (X_2023["ifrs-full_Liabilities"] / X_2023["ifrs-full_Equity"]) * 100
        X_2023["return_on_equity"] = (X_2023["ifrs-full_ProfitLoss"] / X_2023["ifrs-full_Equity"]) * 100
        X_2023["total_asset_turnover"] = X_2023["ifrs-full_Revenue"] / X_2023["ifrs-full_Assets"]
        X_2023["interest_coverage_ratio"] = (X_2023["ifrs-full_ProfitLoss"] / X_2023["ifrs-full_FinanceCosts"]) * 100
        X_2023["revenue_growth_rate"] = ((X_2023["ifrs-full_Assets"] - X_2022["ifrs-full_Assets"]) / X_2022["ifrs-full_Assets"]) * 100

        X_2023 = X_2023.fillna(0)
        
        financial_health_metrics = X_2023.to_dict(orient="records")

    except Exception as e:
        financial_health_metrics = {"error": str(e)}

    return financial_health_metrics
    

def company_detail(request, corp_code):
    """
    기업 상세 정보를 조회하고, 2024년 예측값과 3개 연도의 실제 데이터를 함께 전달하는 뷰
    """
    # 1️⃣ 기업 기본 정보 조회
    company = get_object_or_404(CompanyList, corp_code=corp_code)
    company.a = company.a[7:-4]
    executives = list(CompanyExecutive.objects.filter(corp_code=corp_code).values("name", "position", "birth", "tenure")) 
    workers = list(CompanyWorker.objects.filter(corp_code=corp_code).values("total_staff", "department", "full_time_employee", "contract_worker"))    
    try:
        # 2️⃣ IS, BS, CIS 데이터 가져오기
        is_data = SingleIS.objects.filter(corp_code=corp_code).values("corp_code", "concept_id", "amount_2023", "amount_2022", "amount_2021")
        bs_data = SingleBS.objects.filter(corp_code=corp_code).values("corp_code", "concept_id", "amount_2023", "amount_2022", "amount_2021")
        cis_data = SingleCIS.objects.filter(corp_code=corp_code).values("corp_code", "concept_id", "amount_2023", "amount_2022", "amount_2021")

        # 3️⃣ 데이터프레임 변환
        is_df = pd.DataFrame(list(is_data))
        bs_df = pd.DataFrame(list(bs_data))
        cis_df = pd.DataFrame(list(cis_data))

        # 4️⃣ 모든 데이터를 하나로 합치기
        all_data = pd.concat([is_df, bs_df, cis_df], ignore_index=True)

        # 5️⃣ 2023년 데이터를 기반으로 기업별 피벗 테이블 생성
        pivot_2023 = all_data.pivot_table(index="corp_code", columns="concept_id", values="amount_2023", aggfunc="sum").reset_index()
        pivot_2022 = all_data.pivot_table(index="corp_code", columns="concept_id", values="amount_2022", aggfunc="sum").reset_index()
        pivot_2021 = all_data.pivot_table(index="corp_code", columns="concept_id", values="amount_2021", aggfunc="sum").reset_index()

        # 🔹 `corp_code` 저장 (예측과 결과 매칭용)
        corp_codes = pivot_2023["corp_code"]

        # 6️⃣ 2023년 데이터를 입력값(X)으로 설정 (없는 값은 0으로 채움)
        X_2023 = pivot_2023.reindex(columns=selected_features, fill_value=0)

        # 7️⃣ 저장된 모델로 2024년 예측 수행
        y_pred_2024 = model.predict(X_2023)

        # 8️⃣ "ifrs-full_Revenue" (매출) 값만 필터링하여 실제 매출 저장
        actual_data = pivot_2023[["corp_code"]].copy()
        actual_data["Actual_2023"] = pivot_2023.get("ifrs-full_Revenue", pd.Series([0] * len(pivot_2023)))
        actual_data["Actual_2022"] = pivot_2022.get("ifrs-full_Revenue", pd.Series([0] * len(pivot_2022)))
        actual_data["Actual_2021"] = pivot_2021.get("ifrs-full_Revenue", pd.Series([0] * len(pivot_2021)))

        # 🔹 예측값과 실제값을 합치기
        prediction_results = pd.DataFrame({
            "corp_code": corp_codes,
            "Predicted_2024": y_pred_2024
        })
        final_results = prediction_results.merge(actual_data, on="corp_code")
        
        financial_health_metrics = financial_health(request, corp_code)
        context = {
            "company": company,  # 기업 기본 정보
            "financial_results": final_results.to_dict(orient="records"),  # 2024년 예측 결과 및 실제값
            "financial_health_metrics": financial_health_metrics,  # 재무 건전성 지표 (Hexagon Chart용)
            "workers": workers,
            "executives": executives,
        }

    except Exception as e:
        context = {
            "company": company,
            "error": str(e)
        }

    return render(request, "company_detail.html", context)
 

def decimal_to_float(data):
    """재귀적으로 Decimal 값을 float으로 변환"""
    if isinstance(data, dict):
        return {key: decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    return data

def build_hierarchy(queryset):
    """QuerySet을 계층 구조 JSON 형태로 변환"""
    data = pd.DataFrame.from_records(queryset.values())
    hierarchy = {}

    for _, row in data.iterrows():
        levels = [row["class1"], row.get("class2", None), row.get("class3", None), row.get("class4", None)]
        levels = [level for level in levels if pd.notna(level)]  # NaN 제거

        node = hierarchy
        for level in levels:
            if level not in node:
                node[level] = {}
            node = node[level]

        # 최하위 노드에 값 저장
        node["concept_id"] = row["concept_id"]
        node["amounts"] = {
            "amount_2023": row["amount_2023"],
            "amount_2022": row["amount_2022"],
            "amount_2021": row["amount_2021"],
        }

    return hierarchy


def get_financial_data(request, corp_code, report_type):
    """AJAX 요청을 통해 재무제표 데이터를 반환하는 API 뷰"""
    company = get_object_or_404(CompanyList, corp_code=corp_code)

    if report_type == "BS_single":
        financial_data = SingleBS.objects.filter(corp_code=corp_code)
    elif report_type == "CIS_single":
        financial_data = SingleCIS.objects.filter(corp_code=corp_code)
    elif report_type == "IS_single":
        financial_data = SingleIS.objects.filter(corp_code=corp_code)
    elif report_type == "CF_single":
        financial_data = SingleCF.objects.filter(corp_code=corp_code)
    elif report_type == "BS_connection":
        financial_data = ConnectionBS.objects.filter(corp_code=corp_code)
    elif report_type == "CIS_connection":
        financial_data = ConnectionCIS.objects.filter(corp_code=corp_code)
    elif report_type == "IS_connection":
        financial_data = ConnectionIS.objects.filter(corp_code=corp_code)
    elif report_type == "CF_connection":
        financial_data = ConnectionCF.objects.filter(corp_code=corp_code)
    else:
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    # QuerySet을 계층형 JSON 데이터로 변환
    financial_hierarchy = build_hierarchy(financial_data)

    # Decimal 값을 float으로 변환
    cleaned_data = decimal_to_float(financial_hierarchy)

    return JsonResponse(cleaned_data, safe=False, json_dumps_params={'ensure_ascii': False})
