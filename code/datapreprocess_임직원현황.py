import requests
import json
import os
import csv
import re
from datetime import datetime
import pandas as pd 


# ## 최대주주현황

# def add_column_name():
#     input = './최대주주현황.csv'
#     output = './최대주주현황.csv'

#     rows = []
#     with open (input, 'r', newline='', encoding='utf-8') as f:
#         csv_reader = csv.reader(f)
#         for row in csv_reader:
#             rows.append(row)

#         header = ['status', 'message', 'corp_code', '접수번호', '법인구분', '고유번호', '법인명', '성명',
#                   '관계', '주식종류', '기초소유주식 수', '기초소유쥬식 지분율', 
#                    '기말소유주식 수', '기말소유주식 지분율', '비고', '결산기준일' ]
        
#         with open(output, 'w', newline='', encoding='utf-8') as f:
#             csv_writer = csv.writer(f)
#             csv_writer.writerow(header)
#             csv_writer.writerows(rows)


# add_column_name()


## 임원현황

# 헤더 추가
def add_column_name(input_file, output_file):
    """ CSV 파일에 컬럼명을 추가하는 함수 """
    header = ['status', 'message', 'corp_code', '접수번호', '법인구분', '고유번호', '법인명', '성명', '성별',
              '출생년월', '직위', '등기 임원 여부', '상근여부', '담당업무', '주요경력', '최대주주관계', 
              '재직기간', '임기만료일', '결산기준일']
    
    rows = []
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            rows.append(row)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

# 불필요한 컬럼 삭제
def delete_columns(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        data = list(csv_reader)
    

    delete_columns = {0, 1, 5, 11, 12, 14, 15, 17, 18}
    
    cleaned_data = [
        [col for i, col in enumerate(row) if i not in delete_columns]
        for row in data
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(cleaned_data)
    
    print(f"컬럼 삭제 데이터: {output_file}")

# 나이 전처리
def preprocess_data(file_path):
    """ CSV 데이터를 불러와서 전처리 수행 """
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # 출생연도 추출 및 연령대 계산
    df["출생년월"] = df["출생년월"].replace("-", pd.NA)
    df["출생연도"] = df["출생년월"].astype(str).str[:4]
    df["출생연도"] = pd.to_numeric(df["출생연도"], errors="coerce")
    df = df.dropna(subset=["출생연도"])
    df["age"] = 2025 - df["출생연도"].astype(int)
    df["age_group"] = (df["age"] // 10) * 10
    
    # 법인구분
    corp_cls_mapping = {
        "Y": "유가",
        "K": "코스닥",
        "N": "코넥스",
        "E": "기타"
    }
    df["법인구분"] = df["법인구분"].map(corp_cls_mapping)
    
    return df

# 날짜 전처리
def convert_to_date(date_str):
    if pd.isna(date_str) or date_str.strip() == "":
        return None
    
    patterns = [
        (r'(\d{4})년 (\d{1,2})월 (\d{1,2})일', "%Y-%m-%d"),
        (r'(\d{4})년 (\d{1,2})월', "%Y-%m-%d"),
        (r'(\d{4})\.(\d{1,2})\.(\d{1,2})', "%Y-%m-%d")
    ]
    
    for pattern, date_format in patterns:
        match = re.match(pattern, date_str)
        if match:
            date_str = "-".join(match.groups())
            return datetime.strptime(date_str, date_format)
    
    return None

# 최종 저장
def save_cleaned_data(df, output_file):
    df.to_csv(output_file, index=False, encoding='utf-8')

if __name__ == "__main__":
    input_file = "./임원현황.csv"
    intermediate_file = "./임원현황_with_header.csv"
    cleaned_file = "./임원현황_cleaned.csv"
    
    
    add_column_name(input_file, intermediate_file)
    
    delete_columns(intermediate_file, cleaned_file)
    
    df = preprocess_data(cleaned_file)

    df["재직기간"] = df["재직기간"].astype(str).apply(convert_to_date)
    

    save_cleaned_data(df, "./임원현황_cleaned.csv")

###########################################################################
###########################################################################
###########################################################################
###########################################################################

## 직원현황



# 헤더추가
def add_column_name(input_file, output_file):
    
    rows = []
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            rows.append(row)

    header = ['status', 'message', 'corp_code', '접수번호', '법인구분', '고유번호', '법인명', '사업부문', 
              '성별', '개정전 직원수 정규', '개정전 직원 수 계약', '개정전 직원 기타', '정규직 수', 
              '정규직 단시간 근로자수', '계약직수', '계약직단시간 근로자수', '합계', '평균근속연수', 
              '연간급여총액', '1인평균 금여액', '비고', '결산기준일']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

# 불필요한 컬럼 삭제
def delete_columns(input_file, output_file):
    
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        data = list(csv_reader)

    delete_column_indices = {0, 1, 5, 9, 10, 11, 13, 15, 18, 20, 21}
    
    cleaned_data = [
        [col for i, col in enumerate(row) if i not in delete_column_indices]
        for row in data
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(cleaned_data)

# 결측치 대체, 법인
def preprocess_data(input_file, output_file):
    
    df = pd.read_csv(input_file, encoding='utf-8')

    
    columns_to_process = ["계약직수", "정규직 수", "합계"]
    df[columns_to_process] = df[columns_to_process].replace("-", 0)

    
    df[columns_to_process] = df[columns_to_process].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)

    
    corp_cls_mapping = {
        "Y": "유가",
        "K": "코스닥",
        "N": "코넥스",
        "E": "기타"
    }
    df["법인구분"] = df["법인구분"].map(corp_cls_mapping)


    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"전처리 데이터 저장: {output_file}")

if __name__ == "__main__":
    input_file = "./직원현황.csv"
    temp_file = "./직원현황_temp.csv"
    cleaned_file = "./직원현황_cleaned.csv"

    
    add_column_name(input_file, temp_file)
    delete_columns(temp_file, cleaned_file)
    preprocess_data(cleaned_file, cleaned_file)



###################################################
###################################################
###################################################