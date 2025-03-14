from django.urls import path
from .views import home_view,company_list,company_detail,get_financial_data, financial_health

urlpatterns = [
    path('', home_view, name='home'),
    # path('search/', search_companies, name='search_companies'),  # AJAX 검색 API
    path('companies/', company_list, name='company_list'),
    path('companies/<str:corp_code>/', company_detail, name='company_detail'),
    path("api/financial/<str:corp_code>/<str:report_type>/", get_financial_data, name="get_financial_data"),
    path("api/financial_health/<str:corp_code>/", financial_health, name="financial_health"),
]
