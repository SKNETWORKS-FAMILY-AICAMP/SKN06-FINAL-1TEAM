from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from main.prediction.llm import interactive_forecast
from main.question.llm import process_question_query
from main.summarization.llm import process_summarization_query
import os
# OpenAI 모델 초기화 (GPT-4o-mini r사용)
api_key = os.getenv("OPEN_API_KEY")

# 질문 분류 함수
def classify_question(query,llm):
    prompt = f"""
    사용자의 질문을 "예측", "검색", "요약" 중 하나로 분류하세요.
    반드시 다음 형식으로만 출력하세요: 예측 / 검색 / 요약 (그 외 단어 포함 금지)

    질문: "{query}"
    출력:
    """
    response = llm.invoke(prompt).content.strip()
    print(f"🔎 classify_question 결과: '{response}'")
    return response

# 질문 유형별 처리 함수
def process_question(query,collection, llm):
    return process_question_query(query,collection, llm)

def process_per(query,llm):
    return interactive_forecast(query,llm)

def process_summarization(query,collection,llm):
    return process_summarization_query(query,collection,llm)

# Tool 정의
tools = [
    Tool(
        name="Process Search Question",
        func=process_question,
        description="사용자가 검색을 요청할 경우 실행되는 도구"
    ),
    Tool(
        name="Process Predict Question",
        func=process_per,
        description="사용자가 예측을 요청할 경우 실행되는 도구"
    ),
    Tool(
        name="Process Summarization Question",
        func=process_summarization,
        description="사용자가 요약을 요청할 경우 실행되는 도구"
    ),
]





# 에이전트 초기화
def agent_reset(llm):
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )


# 사용자 질문 처리 함수
def handle_user_query(query,collection, llm):
    category = classify_question(query,llm).strip()
    print(f"🔎 질문 유형: '{category}'")  # 응답 출력

    if category == "검색":
        print("🔎 검색 실행:", query)  # 실행 여부 확인
        response = process_question(query, collection, llm)  # 올바른 함수 실행
        return response
    elif category == "예측":
        print("🔮 예측 실행:", query)
        response = process_per(query,llm)
        return response
    elif category == "요약":
        print("📝 요약 실행:", query)
        return process_summarization(query, collection, llm)
    else:
        return "⚠️ 질문 유형을 분류할 수 없습니다."
    


