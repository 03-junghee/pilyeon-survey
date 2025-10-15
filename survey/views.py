from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Question, Response # Question 모델을 사용하기 위해 import

# 1. 시작 페이지 (Root URL에서 리다이렉트되어 접속됨)
def index(request: HttpRequest) -> HttpResponse:
    """필연 설문조사의 시작 페이지를 렌더링합니다."""
    
    context = {
        'page_title': "필연 : 당신의 이상형을 찾아서",
        'start_button_text': "설문 시작하기"
    }
    # survey/templates/survey/index.html 파일을 보여줍니다.
    return render(request, 'survey/index.html', context)


# 2. 설문 페이지 (응답 처리 로직 포함)
def question_page(request: HttpRequest, page_num: int) -> HttpResponse:
    """
    페이지 번호에 해당하는 질문을 보여주고, 
    POST 요청 시 응답을 처리한 후 다음 페이지로 이동합니다.
    """
    
    # 데이터베이스에서 현재 페이지 번호에 해당하는 질문 객체를 가져옵니다.
    question = get_object_or_404(Question, page_number=page_num)
    
    # 폼 제출(사용자가 A/B 중 선택하고 '다음' 버튼 클릭) 시
    if request.method == 'POST':
        # 폼 데이터에서 사용자의 선택(A 또는 B)을 가져옵니다.
        # HTML 템플릿의 <input name="choice">의 값입니다.
        selected_choice = request.POST.get('choice')
        
        # 만약 선택된 항목이 있다면 (선택 안 하고 제출했을 경우 방지)
        if selected_choice in ['A', 'B']:
            
            # --- [핵심 로직: 사용자 응답 저장] ---
            
            # (1) 세션을 사용하여 임시로 응답을 저장하는 방식 (간단한 설문에서 흔히 사용)
            # 세션에 저장할 설문 응답 딕셔너리를 가져오거나, 없다면 새로 만듭니다.
            user_responses = request.session.get('responses', {})
            
            # 현재 질문 번호(page_num)와 선택한 항목(selected_choice)을 저장합니다.
            user_responses[str(page_num)] = selected_choice
            
            # 변경된 딕셔너리를 다시 세션에 저장합니다.
            request.session['responses'] = user_responses
            # request.session.modified = True # 변경 사항을 확실히 저장하도록 플래그 설정
            
            # --- [핵심 로직 끝] ---
            
            
            # 다음 페이지로 이동할 번호를 계산합니다.
            next_page_num = page_num + 1
            
            # 데이터베이스에 다음 질문이 존재하는지 확인합니다.
            if Question.objects.filter(page_number=next_page_num).exists():
                # 다음 질문 페이지로 리다이렉트합니다.
                return redirect('survey:question_page', page_num=next_page_num)
            else:
                # 8번 질문까지 모두 끝났으므로 결과 페이지로 리다이렉트합니다.
                # 참고: 결과 페이지에서 세션에 저장된 user_responses를 사용해 AI 분석을 진행하게 됩니다.
                return redirect('survey:result')
        
        # 선택이 누락되었을 경우 (선택 안 하고 제출 시)
        # 이 부분은 HTML의 required 속성으로 대부분 처리되지만, 서버에서도 처리할 수 있습니다.
        # 필요하다면 오류 메시지를 context에 담아 현재 페이지를 다시 렌더링할 수 있습니다.
    
    
    # GET 요청 (페이지를 처음 열 때) 또는 POST에서 오류 발생 시
    context = {
        'question': question,
        'current_page': page_num,
        'total_pages': 8 # 총 8개의 질문을 가정
    }
    # survey/templates/survey/question_page.html 파일을 보여줍니다.
    return render(request, 'survey/question_page.html', context)


# ... (다른 함수 및 import는 그대로 둡니다.) ...

# 3. 결과 페이지
def result_page(request: HttpRequest) -> HttpResponse:
    """설문 결과를 분석하여 보여주는 페이지."""
    
    # 세션에서 사용자 응답 데이터를 가져옵니다.
    user_responses = request.session.get('responses', {})
    
    # ------------------ [AI 분석 로직 대체] ------------------
    
    # 1. A/B 선택 개수 계산
    count_a = sum(1 for response in user_responses.values() if response == 'A')
    count_b = sum(1 for response in user_responses.values() if response == 'B')
    
    # 2. 결과 유형 결정 및 아이돌 매칭 (예시)
    
    # A가 5개 이상일 경우 (부드러운, 감성적인 성향)
    if count_a >= 5:
        result_type = "따뜻한 배려형 '순수 연인' 타입"
        matched_idol = "아이유 (IU)"
        idol_description = "섬세한 감수성과 포용력으로 상대를 따뜻하게 안아주는 스타일. 집에서 아늑하게 데이트하는 것을 선호합니다."
        
    # B가 5개 이상일 경우 (주도적인, 이성적인 성향)
    elif count_b >= 5:
        result_type = "당찬 매력의 '활동적인 리더' 타입"
        matched_idol = "방탄소년단 정국"
        idol_description = "매사에 적극적이고, 연애에서도 리드하는 것을 즐기는 스타일. 새로운 경험과 활동적인 데이트를 선호합니다."
        
    # 그 외 (균형 잡힌 성향)
    else:
        result_type = "균형 잡힌 '현실적인 로맨티스트' 타입"
        matched_idol = "수지"
        idol_description = "감정과 이성의 균형을 잘 잡아주는 만능 타입. 때로는 리드하고 때로는 맞춰주는 융통성을 가진 연인입니다."

    # ------------------ [AI 분석 로직 끝] ------------------

    # context에 결과를 담아 템플릿으로 전달합니다.
    context = {
        'result_title': "필연이 찾은 당신의 이상형 분석 결과",
        'result_type': result_type,
        'matched_idol': matched_idol,
        'idol_description': idol_description,
        'response_count_a': count_a,
        'response_count_b': count_b,
        # 'debug_responses': user_responses # 디버깅용 응답 데이터 (배포 시 제거)
    }
    
    # 세션 데이터는 결과를 보여준 후 깔끔하게 제거합니다.
    if 'responses' in request.session:
        del request.session['responses']
        
    # survey/templates/survey/result.html 파일을 렌더링합니다.
    return render(request, 'survey/result.html', context)