# company/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import NewsData
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

def news_list(request):
    query = request.GET.get('search', '').strip()  # 검색어 가져오기 & 공백 제거

    if query:
        # 제목, 신문사, 본문(content_display)에서 검색
        news_list = NewsData.objects.filter(
            Q(title__icontains=query) | 
            Q(newspaper_org__icontains=query) | 
            Q(content_display__icontains=query)
        ).order_by('-pub_date')
    else:
        news_list = NewsData.objects.all().order_by('-pub_date')

    # 페이지네이션 설정
    page = request.GET.get('page', 1)
    paginator = Paginator(news_list, 10)
    page_obj = paginator.get_page(page)

    # 페이지 그룹 계산 (10개 단위)
    current_page = page_obj.number
    total_pages = paginator.num_pages
    group_size = 10
    start_page = ((current_page - 1) // group_size) * group_size + 1
    end_page = min(start_page + group_size - 1, total_pages)
    page_range = range(start_page, end_page + 1)

    context = {
        'page_obj': page_obj,
        'page_range': page_range,
        'total_pages': total_pages,
        'query': query,  # 현재 검색어를 템플릿에 전달
    }
    return render(request, 'news_list.html', context)

def news_detail(request, id):
    news_item = get_object_or_404(NewsData, id=id)

    # keyword_5 값 확인 후 리스트 변환
    if news_item.keyword_5:
        keywords_list = [k.strip() for k in news_item.keyword_5.split(',') if k.strip()]
    else:
        keywords_list = []  # ✅ 빈 리스트 처리

    print(f"DEBUG: keywords_list = {keywords_list}")  # 디버깅용

    return render(request, 'news_detail.html', {
        'news_item': news_item,
        'keywords_list': keywords_list,
        'link_org': news_item.link_org,
    })
