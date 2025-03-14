from django.shortcuts import render
import json,os
from django.conf import settings  # settings.py에서 BASE_DIR 가져오기
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .agent import handle_user_query,agent_reset  # agent.py 가져오기
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from company.models import CompanyList
def home_view(request):
    return render(request, 'home.html')


# OpenAI 모델 초기화
api_key = os.getenv("OPEN_API_KEY")
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
CHROMA_DB_DIR = os.path.join(settings.BASE_DIR,"main","chromadb_store2")
print("CH :",CHROMA_DB_DIR)
# 벡터DB 연결

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
            print("벡벡 :",user_query)
            if not user_query:
                return JsonResponse({"error": "질문을 입력하세요!"}, status=400)

            print(f"📢 사용자 질문: {user_query}")  # 질문 로그 추가

            # LangChain을 활용한 검색 실행
            print("CHASDWQD :", CHROMA_DB_DIR)
            collection = Chroma(
                collection_name="company_docs",
                embedding_function=embedding_model,
                persist_directory=CHROMA_DB_DIR
            )
            agent_reset(llm)
            response = handle_user_query(user_query, collection, llm)

            print(f"📢 LangChain 응답: {response}")  # 결과 로그 추가

            return JsonResponse({"response": response})

        except Exception as e:
            import traceback
            print("🚨 오류 발생:", traceback.format_exc())  # 전체 오류 출력
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST 요청만 지원됩니다."}, status=405)
