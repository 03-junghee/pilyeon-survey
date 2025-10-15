from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect # redirect 함수를 가져옵니다.

# 사용자가 루트 주소('/')로 접속하면 '/survey/'로 리다이렉트(재요청)할 함수
def root_redirect(request):
    return redirect('survey:index') # survey 앱의 'index'라는 이름의 URL로 리다이렉트합니다.

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- 새로 추가할 부분 ---
    path('', root_redirect, name='root'), # 루트 주소(http://127.0.0.1:8000/)에 대한 설정
    # -----------------------
    
    path('survey/', include(('survey.urls', 'survey'), namespace='survey')), # survey URL 패턴 수정
]