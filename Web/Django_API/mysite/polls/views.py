from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'questions': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {'question': question, 'error_message': '선택이 없습니다.'})
    else:
        selected_choice.votes = F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:index'))


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user-list')  # url pattern의 name으로 가져옴
    template_name = 'registration/signup.html'
