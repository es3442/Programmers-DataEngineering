from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'questions': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})


def some_url(request):
    return HttpResponse("Some url을 구현해봤습니다.")
