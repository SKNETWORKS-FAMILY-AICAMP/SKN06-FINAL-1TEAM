from django.db import models

class NewsData(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    newspaper_org = models.CharField(max_length=100)
    content_display = models.TextField(null=True, blank=True)
    keyword_5 = models.TextField()
    link_org = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'cleaned_news_data'
        # 기존 테이블을 그대로 사용
        managed = False
