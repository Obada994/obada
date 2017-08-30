from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from .models import Question, Answer, Choice
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .serializer import AnswerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from .serializer import UserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AnsweresList(APIView):
    def get(self, request):
        answers = Answer.objects.filter(user=request.user)
        serial = AnswerSerializer(answers, many=True)
        return Response(serial.data)

# Create your views here.
def index(request):
    all_questions = Question.objects.all()
    context = {
        'all_questions': all_questions
    }
    return render(request, 'questions/index.html', context)


def question(request, question_id):
    # Just in case the question does not exist
    question = get_object_or_404(Question, pk=question_id)
    all_choices = question.choice_set.all()
    context = {'all_choices': all_choices,
               'question': question}

    return render(request, 'questions/questions.html', context)


def choice(request, question_id, choice_id):
    usr_choice = Choice.objects.get(pk=choice_id)
    # Create an answer object from the user_choice
    usr_answer = Answer(choice=usr_choice, user=request.user)
    # Get all the answers to check if this user has already an answer for the same question
    all_answers = Answer.objects.all()
    for each_answer in all_answers:
        if (each_answer.choice.question == usr_answer.choice.question) and (each_answer.user == usr_answer.user):
            return redirect('error')
    # Up to this point the usr_answer is a new answer.
    usr_answer.save()
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


def error(request):
    return HttpResponse("You already answered that question :)")


def login_view(request):
    pass
