#### csv 기반 기업개요 요약 코드

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import time

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 키 확인
if openai_api_key:
    print("✅ OpenAI API 키가 정상적으로 로드되었습니다.")
else:
    print("❌ OpenAI API 키를 불러오지 못했습니다. .env 파일을 확인하세요.")
    exit()

# OpenAI 모델 설정 (LangChain ChatOpenAI 사용)
chat_model = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=openai_api_key)

def generate_summary_html(company_name, text, retries=5, wait_time=10):
    """OpenAI GPT-4를 이용해 기업 개요 + 사업 개요를 HTML 형식으로 요약"""
    prompt = f"""
    당신은 기업 정보를 HTML 보고서 형식으로 요약하는 AI입니다.  
    출력은 **항상 존댓말을 사용하며, 문장은 "~입니다.", "~합니다."와 같은 다나까 체로 마무리해야 합니다.**  
    **단답형 응답을 피하고, 모든 문장을 일관되게 풀어서 작성하세요.**  
    **문장이 짧아지거나 문맥이 끊기지 않도록 자연스럽게 연결하여 작성하세요.**  
    **항목 간 어조와 서술 방식을 통일하여 기업 개요에 일관성을 유지하세요.**  
    **기업을 지칭할 때 "이 기업", "이 회사"와 같은 표현을 사용하지 말고, 항상 회사명을 정확하게 기재하세요.**
    **요약에 불필요한 지칭이나 서술은 최대한 지양해주세요.**
    **정확한 정보를 토대로 작성해주세요.**

    아래는 한 기업의 핵심 정보입니다. **이 내용을 바탕으로 300자 이내로 간결하고 핵심적인 기업 개요를 작성하세요.** 
    HTML 코드로 반환하며, 모든 출력은 한글로 작성하세요.  
    각 `<p>` 태그에 클래스를 추가하여 스타일링할 수 있도록 하세요.  

    ---  

    ## **출력 형식 (HTML + 클래스 적용)**
    ```html
    <div class="company-report">
        <h2 class="company-name">{company_name} 기업 개요</h2>
        <p class="industry"><strong>산업/업종:</strong> [해당 기업이 속한 산업과 업종을 설명하세요.]</p>
        <p class="business"><strong>핵심 사업:</strong> [기업이 영위하는 주요 사업 내용을 서술하세요.]</p>
        <p class="products"><strong>주요 제품:</strong> [기업이 생산하거나 제공하는 주요 제품 및 서비스를 나열하세요.]</p>
        <p class="market"><strong>주요 시장:</strong> [기업의 주요 고객 및 진출 시장을 설명하세요.]</p>
        <p class="current-status"><strong>현재 상황:</strong> [기업의 최근 경영 현황 및 주요 전략을 포함하세요.]</p>
        <p class="growth"><strong>성장 전망:</strong> [기업의 향후 성장 가능성과 발전 방향을 예측하여 설명하세요.]</p>
    </div>
    ```

    ---  

    ## **기업 핵심 정보**
    - **회사명**: {company_name}  
    - **주요 사업**: {text}  

    ---  

    위의 HTML 형식과 일치하는 코드를 생성하세요.  
    """

    for attempt in range(retries):
        try:
            response = chat_model.invoke([{"role": "system", "content": "당신은 기업 정보를 요약하는 AI입니다."},
                                          {"role": "user", "content": prompt}])
            return response.content.strip()
        except Exception as e:
            print(f"❌ 오류 발생 (시도 {attempt + 1}/{retries}): {e}")
            if "429" in str(e):
                print(f"🔄 {wait_time}초 후 재시도...")
                time.sleep(wait_time)
            else:
                break

    return "<p>요약 생성 실패</p>"

# CSV 파일 로드
csv_file_path = "extracted_reports_updated.csv"
df = pd.read_csv(csv_file_path, encoding="utf-8")

# 회사코드별 데이터 필터링
df_filtered = df[df["제목"].isin(["1. 회사의 개요", "3. 사업의 개요"])]
df_company_names = df[["회사코드", "회사명"]].drop_duplicates()
df_summary = df_filtered.groupby("회사코드")["내용"].apply(lambda x: " ".join(x)).reset_index()
df_summary = df_summary.merge(df_company_names, on="회사코드", how="left")

# OpenAI GPT-4o를 사용해 요약 생성
batch_size = 100
for i in range(0, len(df_summary), batch_size):
    batch = df_summary.iloc[i:i + batch_size].copy()
    batch.loc[:, "요약_HTML"] = batch.apply(lambda row: generate_summary_html(row["회사명"], row["내용"]), axis=1)
    
    # '내용' 컬럼 제거 후 저장
    batch = batch[["회사코드", "회사명", "요약_HTML"]]
    batch.to_csv("summarized_reports.csv", index=False, encoding="utf-8-sig", mode='a', header=(i == 0))
    print(f"✅ {i + batch_size}개 기업 개요 요약 완료!")

print(f"✅ 모든 기업 개요 요약 완료! CSV 저장 위치: summarized_reports.csv")



### Gpt Api 호출하여 검색하는 요약 코드

# import os
# import pandas as pd
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# import time

# # .env 파일 로드
# load_dotenv()

# # 환경 변수에서 API 키 가져오기
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # OpenAI API 키 확인
# if openai_api_key:
#     print("✅ OpenAI API 키가 정상적으로 로드되었습니다.")
# else:
#     print("❌ OpenAI API 키를 불러오지 못했습니다. .env 파일을 확인하세요.")
#     exit()

# # OpenAI 모델 설정 (LangChain ChatOpenAI 사용)
# chat_model = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=openai_api_key)

# # 대상 회사 목록 (회사코드, 회사명)
# companies = [
#     (101044, "에이프로젠바이오로직스"),
#     (102618, "계양전기"),
#     (105961, "LG이노텍"),
#     (113359, "교보증권"),
#     (115676, "KG스틸"),
#     (118284, "동일금속"),
#     (127158, "씨아이테크"),
#     (140168, "HS애드"),
#     (141404, "영풍제지"),
#     (145552, "이수화학"),
#     (146269, "일신방직"),
#     (149026, "CS홀딩스"),
#     (165060, "하이록코리아"),
#     (203290, "콜마홀딩스"),
#     (260958, "케이티알파"),
#     (267906, "베뉴지"),
#     (349097, "케이티스카이라이프"),
#     (389970, "다날"),
#     (439965, "나노신소재"),
#     (483735, "해성옵틱스"),
#     (486370, "성창오토텍"),
#     (602136, "디와이피엔에프"),
#     (607496, "한빛레이저"),
#     (677334, "아하"),
#     (872984, "이마트"),
#     (965813, "미투온"),
#     (989664, "코아스템켐온"),
#     (994994, "나노"),
#     (1021666, "덕산테코피아"),
#     (1118643, "로보쓰리에이아이"),
#     (1165739, "잉글우드랩"),
#     (1243161, "인산가"),
#     (1275665, "리메드"),
#     (1301623, "비씨엔씨"),
#     (1326792, "비투엔"),
#     (1546101, "아이엠티")
# ]

# def generate_summary_html(company_name, retries=5, wait_time=10):
#     """OpenAI GPT-4o를 이용해 기업 개요 + 사업 개요를 HTML 형식으로 요약"""
#     prompt = f"""
#     당신은 기업 정보를 HTML 보고서 형식으로 요약하는 AI입니다.  
#     출력은 **항상 존댓말을 사용하며, 문장은 "~입니다.", "~합니다."와 같은 다나까 체로 마무리해야 합니다.**  
#     **절대 단답형으로 응답하지 말고, 모든 문장을 일관되게 풀어서 작성하세요.**  
#     **문맥이 자연스럽도록 연결하여 작성하세요.**
#     **'~에 종사합니다', '~에 속합니다' 와 같은 어휘는 절대 사용하지 마세요.'**
#     **모든 설명은 회사에 대한 정확한 설명이어야 합니다.**
#     **항목 간 어조와 서술 방식을 통일하여 기업 개요에 일관성을 유지하세요.**  
#     **기업을 지칭할 때 "이 기업", "이 회사"와 같은 표현을 사용하지 말고, 항상 회사명을 정확하게 기재하세요.**
#     **요약에 불필요한 지칭이나 서술은 최대한 지양하고, 직접적인 정보만을 간결하게 전달하세요.**
#     **각 정보는 사실 기반으로 작성하세요.**
#     **산업/업종에 대한 설명만 단답형으로, 동일한 형식으로 작성하세요**
#     **반드시 모든 회사를 같은 서술 형식으로 작성하세요** 

#     아래는 "{company_name}"의 핵심 정보입니다.  
#     **최신 정보를 반영하여 300자 이내로 간결하고 핵심적인 기업 개요를 작성하세요.**  
#     HTML 코드로 반환하며, 모든 출력은 한글로 작성하세요.  
#     각 `<p>` 태그에 클래스를 추가하여 스타일링할 수 있도록 하세요.  

#     ---  

#     ## **출력 형식 (HTML + 클래스 적용)**
#     ```html
#     <div class="company-report">
#         <h2 class="company-name">{company_name} 기업 개요</h2>
#         <p class="industry"><strong>산업/업종:</strong> [해당 기업이 속한 산업과 업종]</p>
#         <p class="business"><strong>핵심 사업:</strong> [주요 사업 및 비즈니스 모델]</p>
#         <p class="products"><strong>주요 제품:</strong> [생산하거나 제공하는 주요 제품 및 서비스]</p>
#         <p class="market"><strong>주요 시장:</strong> [주요 고객 및 진출 시장]</p>
#         <p class="current-status"><strong>현재 상황:</strong> [최근 경영 현황 및 주요 전략]</p>
#         <p class="growth"><strong>성장 전망:</strong> [향후 성장 가능성과 발전 방향]</p>
#     </div>
#     ```

#     ---  

#     위의 HTML 형식과 일치하는 코드를 생성하세요.  
#     """

#     for attempt in range(retries):
#         try:
#             response = chat_model.invoke([{"role": "system", "content": "당신은 기업 정보를 요약하는 AI입니다."},
#                                           {"role": "user", "content": prompt}])
#             return response.content.strip()
#         except Exception as e:
#             print(f"❌ 오류 발생 (시도 {attempt + 1}/{retries}): {e}")
#             if "429" in str(e):
#                 print(f"🔄 {wait_time}초 후 재시도...")
#                 time.sleep(wait_time)
#             else:
#                 break

#     return "<p>요약 생성 실패</p>"

# # OpenAI GPT-4o를 사용해 요약 생성 및 저장
# batch_size = 10  # 10개씩 실행하여 속도 조절
# output_csv_path = "summarized_reports_2.csv"

# for i in range(0, len(companies), batch_size):
#     batch = companies[i:i + batch_size]
    
#     results = []
#     for company_code, company_name in batch:
#         summary_html = generate_summary_html(company_name)
#         results.append((company_code, company_name, summary_html))
    
#     # 결과를 DataFrame으로 변환 후 저장
#     df_batch = pd.DataFrame(results, columns=["회사코드", "회사명", "요약_HTML"])
#     df_batch.to_csv(output_csv_path, index=False, encoding="utf-8-sig", mode='a', header=(i == 0))
    
#     print(f"✅ {i + batch_size}개 기업 개요 요약 완료!")

# print(f"✅ 모든 기업 개요 요약 완료! CSV 저장 위치: {output_csv_path}")
