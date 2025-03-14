# Python 3.10 사용
FROM python:3.12.8

# 컨테이너 내부 작업 디렉토리 (config 폴더로 이동)
WORKDIR /WEB/config

# 프로젝트 파일 복사
COPY . .

# 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

# Django 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


