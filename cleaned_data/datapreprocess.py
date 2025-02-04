import requests
import json
import os
import csv

# 헤더추가

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


# ## 임원현황

# def add_column_name():
#     input = './임원현황.csv'
#     output = './임원현황.csv'

#     rows = []
#     with open (input, 'r', newline='', encoding='utf-8') as f:
#         csv_reader = csv.reader(f)
#         for row in csv_reader:
#             rows.append(row)

#         header = ['status', 'message', 'corp_code', '접수번호', '법인구분', '고유번호', '법인명', '성명', '성별',
#                   '출생년월', '직위', '등기 임원 여부', '상근여부', '담당업무', '주요경력', '최대주주관계', 
#                   '재직기간', '임기만료일', '결산기준일']
        
#         with open(output, 'w', newline='', encoding='utf-8') as f:
#             csv_writer = csv.writer(f)
#             csv_writer.writerow(header)
#             csv_writer.writerows(rows)


# add_column_name()


# ## 직원현황

# def add_column_name():
#     input = './직원현황.csv'
#     output = './직원현황.csv'

#     rows = []
#     with open (input, 'r', newline='', encoding='utf-8') as f:
#         csv_reader = csv.reader(f)
#         for row in csv_reader:
#             rows.append(row)

#         header = ['status', 'message', 'corp_code', '접수번호', '법인구분', '고유번호', '법인명', '사업부문', 
#                   '성별', '개정전 직원수 정규', '개정전 직원 수 계약', '개정전 직원 기타', '정규직 수', 
#                   '정규직 단시간 근로자수', '계약직수', '계약직단시간 근로자수', '합계', '평균근속연수', 
#                   '연간급여총액', '1인평균 금여액', '비고', '결산기준일']
        
#         with open(output, 'w', newline='', encoding='utf-8') as f:
#             csv_writer = csv.writer(f)
#             csv_writer.writerow(header)
#             csv_writer.writerows(rows)


# add_column_name()


###################################################
###################################################
###################################################

# 필요없는 변수 삭제

# ## 임원현황

# def delete_column():
#     input = './임원현황.csv'
#     output = './임원현황_cleaned.csv'

#     with open (input, 'r', newline='', encoding='utf-8') as f:
#             csv_reader = csv.reader(f)
#             data = list(csv_reader)

#     delete_column = [0, 1, 5, 11, 12, 14, 15, 17, 18]
    
#     cleaned_data = [
#           [col for i, col in enumerate(row) if i not in delete_column]
#           for row in data
#     ]

#     with open(output, 'w', newline='', encoding='utf-8') as f:
#           csv_writer = csv.writer(f)
#           csv_writer.writerows(cleaned_data)


# delete_column()

## 직원

def delete_column():
    input = './직원현황.csv'
    output = './직원현황_cleaned.csv'

    with open (input, 'r', newline='', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            data = list(csv_reader)

    delete_column = [0, 1, 5, 9, 10, 11, 13, 15, 18, 20, 21 ]
    
    cleaned_data = [
          [col for i, col in enumerate(row) if i not in delete_column]
          for row in data
    ]

    with open(output, 'w', newline='', encoding='utf-8') as f:
          csv_writer = csv.writer(f)
          csv_writer.writerows(cleaned_data)


delete_column()