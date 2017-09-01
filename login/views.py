from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Question, Answer
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializer import UserSerializer, AnswerSerializer, QuestionSerializer
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
#REST API views here
class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class AnswerViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

def UserAnswers(request):
    if request.method == 'GET':
        answers = Answer.objects.filter(user=request.user)
        serializer = AnswerSerializer(answers, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Question views here.
def Index(request):
    # If the user is not authenticated
    if not request.user.is_authenticated():
        return redirect('signup')
    all_questions = Question.objects.all()
    user_answeres = Answer.objects.filter(user=request.user)
    if len(user_answeres) > 0:
        for answer in user_answeres:
            # Probably there's a smarter way to do it!
            all_questions = all_questions.exclude(pk=answer.choice.question.pk)
        if len(all_questions) == 0:
            return render(request, 'questions/done.html', {})
        else:
            path = reverse('question:question', args=(all_questions[0].id,))
            return redirect(path)
    else:
        path = reverse('question:question', args=(all_questions[0].id,))
        return redirect(path)

def QuestionView(request, question_id):
    # If the user is not authenticated
    if not request.user.is_authenticated():
        return redirect('signup')
    # Just in case the question does not exist
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST['option'])
        except:
            # If the user submits nothing redirect them to the same page
            return redirect(request.path)
        user_answer = Answer(choice=selected_choice, user=request.user)
        user_answer.save()
        return redirect('question:index')

    all_choices = question.choice_set.all()
    context = {'all_choices': all_choices,
               'question': question}

    return render(request, 'questions/question.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('question:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})