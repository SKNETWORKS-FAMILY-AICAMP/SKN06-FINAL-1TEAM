from django.urls import path, include
from .views import home_view,chatbot_api,search_company

urlpatterns = [
    path('', home_view, name='home'),
    path("chat/", chatbot_api, name="chatbot_api"),
    path("search-company/", search_company, name="search_company"),
    path('', include('company.urls')),
]
