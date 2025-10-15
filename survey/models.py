from django.db import models

# 설문 항목(질문)을 정의하는 모델
class Question(models.Model):
    # 질문의 고유 번호 (자동 생성)
    # id = models.AutoField(primary_key=True)

    # 페이지 번호 (1번부터 8번까지)
    page_number = models.IntegerField(unique=True, verbose_name="페이지 번호")
    
    # 질문의 제목 (예: "데이트 방식 선호도")
    question_text = models.CharField(max_length=200, verbose_name="질문 텍스트")
    
    # 질문에 대한 간단한 설명
    description = models.TextField(verbose_name="설명")
    
    # 이지선다의 A 옵션 텍스트 (예: "집에서 영화 보기")
    option_a_text = models.CharField(max_length=100, verbose_name="옵션 A 텍스트")
    
    # 이지선다의 B 옵션 텍스트 (예: "밖에서 활동적인 데이트")
    option_b_text = models.CharField(max_length=100, verbose_name="옵션 B 텍스트")

    # 객체를 문자열로 표시할 때 사용
    def __str__(self):
        return f'{self.page_number}. {self.question_text}'

# 사용자의 응답을 저장하는 모델 (이후에 세션을 통해 응답을 수집할 수도 있지만, 일단 모델 정의)
class Response(models.Model):
    # 나중에 사용자를 식별할 수 있는 필드가 추가될 수 있습니다.
    
    # 어떤 질문에 대한 응답인지 연결
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # 사용자가 A를 선택했으면 'A', B를 선택했으면 'B'로 저장
    selected_option = models.CharField(max_length=1) 
    
    def __str__(self):
        return f'{self.question.question_text}: {self.selected_option}'