from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
# 모델 생성
# 모델을 테이블에 써 추가를 위한 마이그레이션 만든다.
# 모델에 맞는 테이블을 만든다.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    # score=models.FloatField(default=0)
    # is_something_wrong=models.BooleanField(default=False)
    # json_field=models.JSONField(default=dict)

    def was_published_recently(self):  # 어제보다 최근에 만들어진 경우
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):  # 모델 객체 목록에서, 제목과 날짜가 표시
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)  # Foreign_key
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):  # 모델 객체 목록에서, 제목과 날짜가 표시
        return f'[{self.question.question_text}] : {self.choice_text}'
