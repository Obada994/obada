from .models import Answer, Question, Choice
from django.contrib.auth.models import User
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('question_text',)

class ChoiceSerializer(serializers.ModelSerializer):

    question = QuestionSerializer()

    class Meta:
        model = Choice
        fields = ('choice_text', 'question')

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class AnswerSerializer(serializers.ModelSerializer):

    choice = ChoiceSerializer()
    user = UserSerializer()

    class Meta:
        model = Answer
        fields = ('choice', 'user')