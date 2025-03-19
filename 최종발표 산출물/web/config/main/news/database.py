import pymysql,os,requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

def get_news_content():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        query = "SELECT pub_date, content_display, link_org FROM cleaned_news_data"
        cursor.execute(query)
        result = cursor.fetchall()

    conn.close()
    return result