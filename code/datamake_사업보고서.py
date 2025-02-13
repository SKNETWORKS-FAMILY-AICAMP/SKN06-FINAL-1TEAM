import dart_fss as dart
import requests
import json
import os
import csv
from dotenv import load_dotenv
import pandas as pd

# Load API key from environment variables
load_dotenv('../.env')
api_key = os.environ['DART_API_KEY2']


## 자산 증감

# def fetch_cir_status():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3000:4000]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/irdsSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('자산증감.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['isu_dcrs_de'], data['list'][0]['isu_dcrs_stle']
#                                              , data['list'][0]['isu_dcrs_stock_knd'], data['list'][0]['isu_dcrs_qy']
#                                              , data['list'][0]['isu_dcrs_mstvdv_fval_amount'], data['list'][0]['isu_dcrs_mstvdv_amount'], data['list'][0]['stlm_dt']])

# fetch_cir_status()

## 배당에 관한 사항

# def alot_matter():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3400:3600]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('배당사항.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['se']
#                                              , data['list'][0]['thstrm'], data['list'][0]['frmtrm']
#                                              , data['list'][0]['lwfr'], data['list'][0]['stlm_dt']])
                            

# alot_matter()


# ## 자기주식 취득 및 처분 현황

# def tst_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3400]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/tesstkAcqsDspsSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('자기주식취득_처분.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['acqs_mth1']
#                                              , data['list'][0]['acqs_mth2'], data['list'][0]['acqs_mth3']
#                                              , data['list'][0]['bsis_qy'], data['list'][0]['change_qy_acqs']
#                                              , data['list'][0]['change_qy_dsps'], data['list'][0]['change_qy_incnr']
#                                              , data['list'][0]['trmend_qy'], data['list'][0]['rm']
#                                              , data['list'][0]['stlm_dt']])
                            

# tst_stat()


# ## 소액주주 현황

# def shldr_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3400]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/mrhlSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('소액주주현황.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['se']
#                                              , data['list'][0]['shrholdr_co'], data['list'][0]['shrholdr_tot_co']
#                                              , data['list'][0]['shrholdr_rate'], data['list'][0]['hold_stock_co']
#                                              , data['list'][0]['stock_tot_co'], data['list'][0]['hold_stock_rate']
#                                              , data['list'][0]['stlm_dt']])
                            

# shldr_stat()


# ## 임원 현황

# def exct_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3830]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/exctvSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('임원현황.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             for entry in data['list']:
#                                  writer.writerow([data['status'], data['message'], c[2],
#                                                    entry.get('rcept_no', 'NA'), 
#                                                    entry.get('corp_cls'), 
#                                                    entry.get('corp_code'),
#                                                    entry.get('corp_name'),
#                                                    entry.get('nm'), 
#                                                    entry.get('sexdstn'),
#                                                    entry.get('birth_ym'),
#                                                    entry.get('ofcps'),
#                                                    entry.get('rgist_exctv_at'),
#                                                    entry.get('fte_at'),
#                                                    entry.get('chrg_job'),
#                                                    entry.get('main_career'),
#                                                    entry.get('mxmm_shrholdr_relate'),
#                                                    entry.get('hffc_pd'),
#                                                    entry.get('tenure_end_on'),
#                                                    entry.get('stlm_dt')])
            
                            
# exct_stat()




# ## 최대주주 현황

# def hyslr_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3400:3830]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/hyslrSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('최대주주현황.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             for entry in data['list']:
#                                  writer.writerow([data['status'], data['message'], c[2],
#                                                    entry.get('rcept_no'), 
#                                                    entry.get('corp_cls'), 
#                                                    entry.get('corp_code'),
#                                                    entry.get('corp_name'), 
#                                                    entry.get('nm'),
#                                                    entry.get('relate'),
#                                                    entry.get('stock_kind'),
#                                                    entry.get('bsis_posesn_stock_co'),
#                                                    entry.get('bsis_posesn_stock_qota_rt'),
#                                                    entry.get('trmend_posesn_stock_co'),
#                                                    entry.get('trmend_posesn_stock_qota_rt'),
#                                                    entry.get('rm'),
#                                                    entry.get('stlm_dt')])
            
                            
# hyslr_stat()


# ## 직원 현황

# def emp_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3830]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/empSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('직원현황.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             for entry in data['list']:
#                                  writer.writerow([data['status'], data['message'], c[2],
#                                                    entry.get('rcept_no'), 
#                                                    entry.get('corp_cls'), 
#                                                    entry.get('corp_code'),
#                                                    entry.get('corp_name'), 
#                                                    entry.get('fo_bbm'),
#                                                    entry.get('sexdstn'),
#                                                    entry.get('reform_bfe_emp_co_rgllbr'),
#                                                    entry.get('reform_bfe_emp_co_cnttk'),
#                                                    entry.get('reform_bfe_emp_co_etc'),
#                                                    entry.get('rgllbr_co'),
#                                                    entry.get('rgllbr_abacpt_labrr_co'),
#                                                    entry.get('cnttk_co'),
#                                                    entry.get('cnttk_abacpt_labrr_co'),
#                                                    entry.get('sm'),
#                                                    entry.get('avrg_cnwk_sdytrn'),
#                                                    entry.get('fyer_salary_totamt'),
#                                                    entry.get('jan_salary_am'),
#                                                    entry.get('rm'),
#                                                    entry.get('stlm_dt'),])

# emp_stat()


# ## 이사·감사의 개인별 보수현황(5억원 이상)

# def dac_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3400]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/hmvAuditIndvdlBySttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('이사감사보수현황_5억이상.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['nm']
#                                              , data['list'][0]['ofcps'], data['list'][0]['mendng_totamt']
#                                              , data['list'][0]['mendng_totamt_ct_incls_mendng'], data['list'][0]['stlm_dt']])
                            

# dac_stat()



# ## 개인별 보수지급 금액(5억원 이상)

# def indslry_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3400]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/indvdlByPay.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('개인_보수_금액(5억이상).csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['nm']
#                                              , data['list'][0]['ofcps'], data['list'][0]['mendng_totamt']
#                                              , data['list'][0]['mendng_totamt_ct_incls_mendng'], data['list'][0]['stlm_dt']])
                            

# indslry_stat()

# ## 타법인 출자현황

# def invtmt_stat():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3300:3400]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/otrCprInvstmntSttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('타법인_출자현황.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['inv_prm']
#                                              , data['list'][0]['frst_acqs_de'], data['list'][0]['invstmnt_purps']
#                                              , data['list'][0]['frst_acqs_amount'], data['list'][0]['bsis_blce_qy']
#                                              , data['list'][0]['bsis_blce_qota_rt'], data['list'][0]['bsis_blce_acntbk_amount']
#                                              , data['list'][0]['incrs_dcrs_acqs_dsps_qy'], data['list'][0]['incrs_dcrs_acqs_dsps_amount']
#                                              , data['list'][0]['incrs_dcrs_evl_lstmn'], data['list'][0]['trmend_blce_qy']
#                                              , data['list'][0]['trmend_blce_qota_rt'], data['list'][0]['trmend_blce_acntbk_amount']
#                                              , data['list'][0]['recent_bsns_year_fnnr_sttus_tot_assets'], data['list'][0]['recent_bsns_year_fnnr_sttus_thstrm_ntpf']
#                                              , data['list'][0]['stlm_dt']])
                            

# invtmt_stat()

# ## 주식의 총수 현황

# def stock_total_qy():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3218:3400]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/stockTotqySttus.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('주식총수_현황.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['se']
#                                              , data['list'][0]['isu_stock_totqy'], data['list'][0]['now_to_isu_stock_totqy']
#                                              , data['list'][0]['now_to_dcrs_stock_totqy'], data['list'][0]['redc']
#                                              , data['list'][0]['profit_incnr'], data['list'][0]['rdmstk_repy']
#                                              , data['list'][0]['etc'], data['list'][0]['istc_totqy']
#                                              , data['list'][0]['tesstk_co'], data['list'][0]['distb_stock_co']
#                                              , data['list'][0]['stlm_dt']])
                            

# stock_total_qy()


# ## 채무증권 발행실적

# def detisu():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[3200:3300]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/detScritsIsuAcmslt.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('채무증권_발행실적.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['isu_cmpny']
#                                              , data['list'][0]['scrits_knd_nm'], data['list'][0]['isu_mth_nm']
#                                              , data['list'][0]['isu_de'], data['list'][0]['facvalu_totamt']
#                                              , data['list'][0]['intrt'], data['list'][0]['evl_grad_instt']
#                                              , data['list'][0]['mtd'], data['list'][0]['repy_at']
#                                              , data['list'][0]['mngt_cmpny'], data['list'][0]['stlm_dt']])
                            

# detisu()



# ## 기업어음증권 미상환 잔액

# def corp_nrblce():
#     with open('./all_company.csv', 'r', newline='') as f:
#             csv_reader = csv.reader(f)
#             com_data = list(csv_reader)[1:100]
#             for c in com_data :
#                 res = requests.get('https://opendart.fss.or.kr/api/entrprsBilScritsNrdmpBlce.json?crtfc_key=' + api_key + '&corp_code='+c[2]+'&bsns_year=2023&reprt_code=11011')
#                 if res.status_code == 200:
#                     data = json.loads(res.text)
#                     if data['status'] == '000' :
#                         print(data)
#                         with open('기업어음_미상환잔액.csv', 'a', newline='') as file:
#                             writer = csv.writer(file)
#                             writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
#                                              , data['list'][0]['corp_name'], data['list'][0]['remndr_exprtn1']
#                                              , data['list'][0]['remndr_exprtn2'], data['list'][0]['de10_below']
#                                              , data['list'][0]['de10_excess_de30_below'], data['list'][0]['de30_excess_de90_below']
#                                              , data['list'][0]['de90_excess_de180_below'], data['list'][0]['de180_excess_yy1_below']
#                                              , data['list'][0]['yy1_excess_yy2_below'], data['list'][0]['yy2_excess_yy3_below']
#                                              , data['list'][0]['yy3_excess'], data['list'][0]['sm']
#                                              , data['list'][0]['stlm_dt']])
                            

# corp_nrblce()


# ## CF(현금흐름표)

# def cf(output_csv="CF.csv", batch_size=300):

#     dart.set_api_key(api_key=api_key)

#     reports = dart.filings.search(bgn_de='20230101', pblntf_detail_ty='a001')

#     corp_dict = {}
#     for report in reports:
#         corp_dict[report.corp_code] = report.corp_name

#     corp_list = list(corp_dict.items())

#     total_corps = len(corp_list)

#     first_batch = True

#     for start_idx in range(0, total_corps, batch_size):
#         batch = corp_list[start_idx:start_idx + batch_size]

#         batch_data = []

#         for corp_code, corp_name in batch:
#             reports = dart.filings.search(corp_code=corp_code, bgn_de='20230101', pblntf_detail_ty='a001')

#             report = report[0]

#             xbrl = report.xbrl

#             cf_list = xbrl.get_cash_flows()

#             cf = cf_list[0]

#             df = cf.to_DataFrame()

#             df.insert(0, "기업명", corp_name)
#             df.insert(1, "기업코드", corp_code)

#             batch_data.append(df)

#         if batch_data:
#             batch_df = pd.concat(batch_data, ignore_index=True)

            
#             batch_df.to_csv(output_csv, mode='w' if first_batch else 'a', encoding="utf-8-sig", index=False, header=first_batch)
#             first_batch = False 

# cf()


############dart.filings.search()에서 corp_code 없이 전체 기업의 데이터를 검색하려 하면 최대 3개월 데이터만 조회 가능.




def cf():
    with open('./보고서 번호.csv', 'r', newline='') as f:
            csv_reader = csv.reader(f)
            com_data = list(csv_reader)[1:100]
            for c in com_data :
                res = requests.get('https://opendart.fss.or.kr/api/fnlttXbrl.xml?crtfc_key=' + api_key + '&rcept_no='+c[2]+'&reprt_code=11011')
                if res.status_code == 200:
                    data = json.loads(res.text)
                    if data['status'] == '000' :
                        print(data)
                        with open('cf.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([c[0], c[1], c[2], data['list'][0]['rcept_no'], data['list'][0]['corp_cls'], data['list'][0]['corp_code']
                                             , data['list'][0]['corp_name'], data['list'][0]['remndr_exprtn1']
                                             , data['list'][0]['remndr_exprtn2'], data['list'][0]['de10_below']
                                             , data['list'][0]['de10_excess_de30_below'], data['list'][0]['de30_excess_de90_below']
                                             , data['list'][0]['de90_excess_de180_below'], data['list'][0]['de180_excess_yy1_below']
                                             , data['list'][0]['yy1_excess_yy2_below'], data['list'][0]['yy2_excess_yy3_below']
                                             , data['list'][0]['yy3_excess'], data['list'][0]['sm']
                                             , data['list'][0]['stlm_dt']])
                            

cf()