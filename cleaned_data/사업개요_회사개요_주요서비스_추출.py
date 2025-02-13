import os
import csv
import re

def load_report_numbers(csv_path):
    """보고서번호.csv 파일을 직접 읽어서 보고서 번호와 고유번호를 매핑"""
    report_mapping = {}

    if not os.path.exists(csv_path):
        print(f"❌ '{csv_path}' 파일이 없습니다. 경로를 확인하세요.")
        return report_mapping  # 빈 딕셔너리 반환
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # 첫 번째 줄(헤더) 읽기
        
        # "보고서 번호"와 "고유번호" 컬럼의 인덱스 찾기
        try:
            report_number_index = header.index("보고서 번호")
            unique_id_index = header.index("고유번호")
        except ValueError:
            print("❌ CSV 파일에서 '보고서 번호' 또는 '고유번호' 컬럼을 찾을 수 없습니다.")
            return report_mapping

        for row in reader:
            report_number = row[report_number_index].strip()  # 보고서 번호
            unique_id = row[unique_id_index].strip().zfill(8)  # 고유번호 (8자리 유지)
            report_mapping[report_number] = unique_id  # 매핑 딕셔너리에 저장
    
    print(f"✅ '{csv_path}' 파일이 정상적으로 로드되었습니다. 총 {len(report_mapping)}개의 보고서 번호가 매핑되었습니다.")
    return report_mapping

def extract_report_from_files():
    input_folder = "xml_files"  # XML 파일이 저장된 폴더
    output_csv = "extracted_reports.csv"  # 최종 저장될 CSV 파일
    report_csv_path = "보고서번호.csv"  # 보고서번호.csv 파일 경로

    # 폴더 및 파일 확인
    if not os.path.exists(input_folder):
        print(f"❌ XML 폴더 '{input_folder}'가 존재하지 않습니다.")
        return
    
    xml_files = [f for f in os.listdir(input_folder) if f.endswith(".xml")]
    
    if not xml_files:
        print(f"❌ XML 파일이 '{input_folder}' 폴더에 없습니다.")
        return
    
    print(f"✅ '{input_folder}' 폴더에서 {len(xml_files)}개의 XML 파일을 찾았습니다.")

    # 보고서 번호 <-> 고유번호 매핑 로드
    report_mapping = load_report_numbers(report_csv_path)
    if not report_mapping:
        print("❌ 보고서 번호 매핑이 없습니다. CSV 파일을 확인하세요.")
        return

    # CSV 파일 초기화 및 헤더 작성
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["리포트번호", "회사코드", "제목", "내용"])  # 고유번호 포함

    # xml_files 폴더 내 모든 XML 파일 처리
    for filename in xml_files:
        report_number = filename.split(".")[0]  # 파일명에서 보고서 번호 추출
        unique_id = report_mapping.get(report_number, "Unknown")  # 고유번호 가져오기

        report_path = os.path.join(input_folder, filename)

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                xml_text = f.read()

                # XML 내부 데이터 일부 출력 (디버깅용)
                print(f"🔍 {report_number}.xml 첫 500자:\n{xml_text[:800]}\n")

                # 1. 회사의 개요 섹션 추출
                start_idx1 = xml_text.find('1. 회사의 개요</TITLE>')
                end_idx1 = xml_text.find('2. 회사의 연혁</TITLE>')

                biz_res1 = xml_text[start_idx1:end_idx1] if start_idx1 != -1 and end_idx1 != -1 else "Could not find"

                # 2. 주요 제품 및 서비스 섹션 추출
                start_idx2 = xml_text.find('2. 주요 제품 및 서비스</TITLE>')
                end_idx2 = xml_text.find('3. 원재료 및 생산설비</TITLE>')

                biz_res2 = xml_text[start_idx2:end_idx2] if start_idx2 != -1 and end_idx2 != -1 else "Could not find"

                # 3. 사업의 개요 섹션 추출 (추가된 기능)
                start_idx3 = xml_text.find('1. 사업의 개요</TITLE>')
                end_idx3 = xml_text.find('2. 주요 제품 및 서비스</TITLE>')

                biz_res3 = xml_text[start_idx3:end_idx3] if start_idx3 != -1 and end_idx3 != -1 else "Could not find"

                # HTML 태그 제거 및 정리
                biz_res1_clean = re.sub(r'<[^>]+>', '', biz_res1).replace("\n", " ")
                biz_res2_clean = re.sub(r'<[^>]+>', '', biz_res2).replace("\n", " ")
                biz_res3_clean = re.sub(r'<[^>]+>', '', biz_res3).replace("\n", " ")

                # CSV 파일에 저장 (고유번호 포함)
                with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([report_number, unique_id, "1. 회사의 개요", biz_res1_clean])
                    csv_writer.writerow([report_number, unique_id, "2. 주요 제품 및 서비스", biz_res2_clean])
                    csv_writer.writerow([report_number, unique_id, "3. 사업의 개요", biz_res3_clean])

                print(f"✅ {report_number}.xml 처리 완료! (고유번호: {unique_id})")

        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {report_path}")
        except Exception as e:
            print(f"❌ 오류 발생 ({report_number}.xml): {e}")

# 실행
if __name__ == "__main__":
    try:
        extract_report_from_files()
    except Exception as e:
        print(f"❌ 코드 실행 중 오류 발생: {e}")
