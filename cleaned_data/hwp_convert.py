from PyPDF2 import PdfReader
import pandas as pd

# PDF 파일 경로 설정
pdf_file_path = "C:/Users/Playdata/Desktop/datafile/재무회계개념체계.pdf"  # PDF 파일 경로 수정
csv_file_path = "C:/Users/Playdata/Desktop/datafile/재무회계개념체계.csv"

# PDF 파일에서 모든 텍스트 추출
pdf_reader = PdfReader(pdf_file_path)
text_data = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]

# 추출된 텍스트를 DataFrame으로 변환
df = pd.DataFrame({"내용": text_data})

# CSV 파일로 저장
df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")

print(f"✅ PDF 파일이 CSV로 변환되었습니다: {csv_file_path}")

