from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    # score=models.FloatField(default=0)
    # is_something_wrong=models.BooleanField(default=False)
    # json_field=models.JSONField(default=dict)

    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):  # 모델 객체 목록에서, 제목과 날짜가 표시
        return f'제목: {self.question_text}, 날짜: {self.pub_date}'


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)  # Foreign_key
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):  # 모델 객체 목록에서, 제목과 날짜가 표시
        return f'[{self.question.question_text}] : {self.choice_text}'
