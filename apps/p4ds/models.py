from django.db import models
from django.contrib.auth.models import AbstractUser

class Answers(models.Model):
    question_id = models.CharField(primary_key=True, max_length=20, db_comment='문제 번호 최대 5자리 숫자와 최대 6자의 조합. 예;25876_160952')
    answer_filename = models.CharField(max_length=255, blank=True, null=True, db_comment='답안 파일명 학년_학기_단원_id.png 형식의 파일명. 예:P3_1_02_25876_160952_A.png')
    answer_correct = models.TextField(blank=True, null=True, db_comment='모범답안 정답')
    answer_text = models.TextField(blank=True, null=True, db_comment='모범답안 풀이')
    source = models.CharField(max_length=255, blank=True, null=True, db_comment='데이터 출처')
    label = models.CharField(max_length=255, blank=True, null=True, db_comment='데이터 용도 training/validation')

    class Meta:
        managed = False
        db_table = 'answers'
        db_table_comment = '모범답안'

class ConceptMapping(models.Model):
    question_topic = models.IntegerField(primary_key=True, db_comment='문제 토픽 주제 번호(문제생성 데이터)')  # The composite primary key (question_topic, concept_id) found, that is not supported. The first column is selected.
    concept_id = models.IntegerField(db_comment='단원 번호(학습자 역량측정 데이터)')
    question_topic_name = models.CharField(max_length=255, blank=True, null=True, db_comment='토픽명 텍스트(문제생성 데이터)')
    concept_name = models.CharField(max_length=255, blank=True, null=True, db_comment='단원명(예:직각삼각형의 합동 조건)')
    concept_semester = models.CharField(max_length=50, blank=True, null=True, db_comment='학기(예:중등-중2-2학기)')
    concept_description = models.TextField(blank=True, null=True, db_comment='단원 설명')
    concept_chapter_id = models.CharField(max_length=50, blank=True, null=True, db_comment='단원 분류 아이디')
    concept_chapter_name = models.CharField(max_length=255, blank=True, null=True, db_comment='단원 분류 내용(예:도형의 성질 > 삼각형의 성질 > 직각삼각형의 합동조건)')
    concept_achievement_id = models.CharField(max_length=50, blank=True, null=True, db_comment='성취 목표 번호')
    concept_achievement_name = models.CharField(max_length=255, blank=True, null=True, db_comment='성취 목표 내용(예:삼각형의 합동 조건을 이해하고 두 삼각형이 합동인지 판별할 수 있다.)')
    from_concept_id = models.IntegerField(blank=True, null=True, db_comment='선행 단원 번호')
    to_concept_id = models.IntegerField(blank=True, null=True, db_comment='후행 단원 번호')

    class Meta:
        managed = False
        db_table = 'concept_mapping'
        unique_together = (('question_topic', 'concept_id'),)
        db_table_comment = '단원 매핑'

class QuestionHistory(models.Model):
    question_set_id = models.IntegerField(primary_key=True, db_comment='문제집 번호(testID)')  # The composite primary key (question_set_id, question_seq) found, that is not supported. The first column is selected.
    question_seq = models.IntegerField(db_comment='문제집 내 문제 순서')
    question_id = models.CharField(max_length=20, db_comment='문제 번호(assessmentItemID)')
    user_no = models.IntegerField(db_comment='사용자 식별 번호(learnerID)')
    is_correct = models.IntegerField(db_comment='정답 여부 (1:정답, 0:오답)')
    created_at = models.DateField(blank=True, null=True, db_comment='풀이 이력 생성 시간')

    class Meta:
        managed = False
        db_table = 'question_history'
        unique_together = (('question_set_id', 'question_seq'),)
        db_table_comment = '풀이 이력'


class QuestionSet(models.Model):
    question_set_id = models.AutoField(primary_key=True, db_comment='문제집 번호(자동부여)')  # The composite primary key (question_set_id, question_seq) found, that is not supported. The first column is selected.
    question_seq = models.IntegerField(db_comment='문제집 내 문제 순서')
    question_id = models.CharField(max_length=20, db_comment='문제 번호')
    user_no = models.IntegerField(db_comment='사용자 식별 번호')
    is_completed = models.IntegerField(blank=True, null=True, db_comment='학습 완료 여부 (1:완료, 0: 미완료)')
    correct_probability = models.FloatField(blank=True, null=True, db_comment='문제 정답 확률')

    class Meta:
        managed = False
        db_table = 'question_set'
        unique_together = (('question_set_id', 'question_seq'),)
        db_table_comment = '생성된 문제집 내역'


class Questions(models.Model):
    question_id = models.CharField(primary_key=True, max_length=20, db_comment='문제 번호 최대 5자리 숫자와 최대 6자의 조합. 예;25876_160952')
    question_filename = models.CharField(max_length=255, blank=True, null=True, db_comment='문제 파일명 학년_학기_단원_id.png 형식의 파일명. 예:P3_1_02_25876_160952.png')
    question_grade = models.CharField(max_length=10, blank=True, null=True, db_comment='문제 학년 (예: P3~P6, M1~M3, H)')
    question_term = models.IntegerField(blank=True, null=True, db_comment='문제 학기 (1 또는 2)')
    question_unit = models.CharField(max_length=10, blank=True, null=True, db_comment='문제 단원 (01~99)')
    question_topic = models.IntegerField(blank=True, null=True, db_comment='문제 토픽 주제 (1~999999)')
    question_topic_name = models.CharField(max_length=255, blank=True, null=True, db_comment='토픽명 텍스트')
    question_type1 = models.CharField(max_length=10, blank=True, null=True, db_comment='문제 유형1 (단답형, 선택형)')
    question_type2 = models.IntegerField(blank=True, null=True, db_comment='발문 구성 유형 (1: 자료+질문, 2: 단일질문)')
    question_condition = models.IntegerField(blank=True, null=True, db_comment='풀이 필수 조건 (0: 없음, 1: 있음)')
    question_step = models.CharField(max_length=10, blank=True, null=True, db_comment='학습 단계 (기본/실생활 활용)')
    question_sector1 = models.CharField(max_length=10, blank=True, null=True, db_comment='평가 영역1 (예: 계산/이해/추론/문제해결)')
    question_sector2 = models.CharField(max_length=255, blank=True, null=True, db_comment='내용 영역 (예: 수와 연산, 도형과 측정, 변화와 관계, 자료와 가능성)')
    question_difficulty = models.IntegerField(blank=True, null=True, db_comment='출제 난이도 (1: 상, 2: 중, 3: 하)')
    question_contents = models.IntegerField(blank=True, null=True, db_comment='문제 내용 (0: 없음, 1: 있음)')
    figure_text = models.TextField(blank=True, null=True, db_comment='도형 설명 텍스트 (optional)')
    question_text = models.TextField(blank=True, null=True, db_comment='문제 텍스트')
    source = models.CharField(max_length=255, blank=True, null=True, db_comment='데이터 출처')
    label = models.CharField(max_length=255, blank=True, null=True, db_comment='데이터 용도 training/validation')

    class Meta:
        managed = False
        db_table = 'questions'
        db_table_comment = '문제'


class Users(AbstractUser):
    user_no = models.AutoField(primary_key=True, db_comment='사용자 식별 번호(자동부여)')
    user_id = models.CharField(unique=True, max_length=50, db_comment='로그인 아이디')
    # password = models.CharField(max_length=255, db_comment='로그인 비밀번호')
    # username = models.CharField(max_length=100, blank=True, null=True, db_comment='이름')
    role = models.IntegerField(blank=True, null=True, db_comment='역할 (1: 학생, 2: 선생님)')
    # email = models.CharField(max_length=100, blank=True, null=True, db_comment='이메일')
    phone = models.CharField(max_length=20, blank=True, null=True, db_comment='전화번호')
    gender = models.IntegerField(blank=True, null=True, db_comment='성별 (1: 남성, 2: 여성)')
    school_name = models.CharField(max_length=100, blank=True, null=True, db_comment='학교명')
    user_grade = models.CharField(max_length=20, blank=True, null=True, db_comment='학년')
    created_at = models.DateField(auto_now_add=True, db_comment='가입일자')  # auto_now_add로 자동 날짜 설정

    USERNAME_FIELD = 'user_id'

    class Meta:
        managed = True
        db_table = 'users'
        db_table_comment = '사용자'
