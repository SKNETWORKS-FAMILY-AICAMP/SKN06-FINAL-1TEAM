# 20240311000132.xml
import csv
import re

def extract_report(): 
    report = './20240311000132.xml'
    output = './extracted_report.csv'

    try:
        with open(report, 'r', encoding='utf-8') as f:
            xml_text = f.read()

            start_idx = xml_text.find('1. 회사의 개요</TITLE>')
            end_idx = xml_text.find('2. 회사의 연혁</TITLE>')

            if start_idx != -1 and end_idx != -1:
                biz_res = xml_text[start_idx:end_idx]
            else:
                biz_res = "Could not find"

            biz_res_clean = re.sub(r'<[^>]+>', '', biz_res)
            biz_res_clean = biz_res_clean.replace("\n", " ")
            
            with open(output, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Extracted Report"])
                csv_writer.writerow([biz_res_clean])

    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."
    except Exception as e:
        return f"오류 발생: {e}"



extract_report()