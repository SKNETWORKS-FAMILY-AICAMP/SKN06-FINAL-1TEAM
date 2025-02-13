import dart_fss as dart
import os
from dotenv import load_dotenv
import csv
import requests
import json
import FinanceDataReader as fdr

load_dotenv('../.env')
api_key= os.environ['DART_API_KEY']

# 상장된 전체 기업 정보 데이터 csv로 저장
def get_corp_list():
    df_krx = fdr.StockListing('KRX')
    df_krx.to_csv('corp_list.csv')

def get_crop_data_by_code() :
    with open('corp_list.csv', 'r', newline='') as f:
        corp_list = f.readlines()
        for corp in corp_list :
            code = corp.split(',')[1].strip()
            # company
            res = requests.get('https://opendart.fss.or.kr/api/company.json?crtfc_key=' + api_key + '&corp_code='+code)
            if res.status_code == 200:

                with open('corp_disclosure_information.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    company = json.loads(res.text)
                    for c in company:
                        writer.writerow(company[c])

                    # company = company['corp_name'], company['corp_name_eng'], company['stock_name'], company['stock_code'],company['ceo_nm'], company['corp_cls'],company['jurir_no'], company['bizr_no'], company['adres'], company['hm_url'], company['ir_url'], company['phn_no'], company['fax_no'],company['fax_no'], company['induty_code'], company['est_dt'], company['acc_mt']]

                # with open('corp_disclosure_information.csv', 'a', newline='') as file:
                #     writer = csv.writer(file)
                #     writer.writerow(['고유번호', '종목명(법인명)', '종목코드', '법인구분', '보고서명', '접수번호', '접수일자', '공시 제출인명', '비고'])
                #     for d in data['list']:
                #         writer.writerow([d['corp_code'], d['corp_name'], d['stock_code'], d['corp_cls'], d['report_nm'], d['rcept_no'], d['rcept_dt'], d['flr_nm'], d['rm']])


# def get_crop_info_by_code():
#     res = requests.get('https://opendart.fss.or.kr/api/list.json?crtfc_key='+api_key+'&page_count=100&page_no=1')
#     if res.status_code == 200:
#         data = json.loads(res.text)
#         with open('corp_disclosure_information.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['고유번호', '종목명(법인명)', '종목코드', '법인구분', '보고서명', '접수번호', '접수일자', '공시 제출인명', '비고'])
#             for d in data['list']:
#                 writer.writerow([d['corp_code'], d['corp_name'], d['stock_code'], d['corp_cls'], d['report_nm'], d['rcept_no'], d['rcept_dt'], d['flr_nm'], d['rm']])


get_corp_list()