from django.urls import path
from . import views

urlpatterns = [
    # 시작 페이지
    path('', views.index, name='index'), 
    
    # 설문 페이지 (예: /survey/1/, /survey/2/ 등)
    # <int:page_num>으로 페이지 번호를 받아서 views.question_page 함수에 전달합니다.
    path('<int:page_num>/', views.question_page, name='question_page'),
    
    # 결과 페이지
    path('result/', views.result_page, name='result'),
]