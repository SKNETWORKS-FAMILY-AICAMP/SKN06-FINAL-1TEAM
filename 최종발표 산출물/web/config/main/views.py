from django.shortcuts import render
import json,os,markdown
from django.conf import settings  # settings.py에서 BASE_DIR 가져오기
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .agent import handle_user_query,agent_reset  # agent.py 가져오기
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from company.models import CompanyList
from langchain.embeddings import HuggingFaceEmbeddings

def home_view(request):
    return render(request, 'home.html')


# OpenAI 모델 초기화
api_key = os.getenv("OPEN_API_KEY")
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key)

embedding_model = HuggingFaceEmbeddings(model_name="FinLang/finance-embeddings-investopedia")


CHROMA_DB_DIR = os.path.join(settings.BASE_DIR,"main","chromadb_FinLang")

def search_company(request):
    keyword = request.GET.get("keyword", "").strip()  # 🔹 검색어 가져오기
    print("baekbaek: ",keyword)
    if len(keyword) < 2:
        return JsonResponse({"data": []})  # 🔹 검색어가 2글자 미만이면 빈 결과 반환

    # 🔹 기업명에 검색어가 포함된 데이터 가져오기
    results = CompanyList.objects.filter(stock_name__icontains=keyword).values("corp_code", "stock_name")

    return JsonResponse({"data": list(results)})  # 🔹 JSON 형식으로 반환


 
@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get("message")
            if not user_query:
                return JsonResponse({"error": "질문을 입력하세요!"}, status=400)

            # LangChain을 활용한 검색 실행
            collection = Chroma(
                collection_name="company_docs",
                embedding_function=embedding_model,
                persist_directory=CHROMA_DB_DIR
            )
            agent_reset(llm)
            response = handle_user_query(user_query, collection, llm)

            # 🔹 마크다운을 HTML로 변환 (extra 확장 사용)
            response_html = markdown.markdown(response, extensions=["extra"])

            return JsonResponse({"response": response_html})  # HTML 그대로 반환

        except Exception as e:
            import traceback
            print("🚨 오류 발생:", traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST 요청만 지원됩니다."}, status=405)