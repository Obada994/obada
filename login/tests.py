from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse

from .models import Question, Choice
from .views import question


class QuestionTest(TestCase):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user('test_user')

        self.question = Question.objects.create(question_text='Which programming language do you like the most?')
        self.choice1 = Choice.objects.create(choice_text="Python", question=self.question)
        self.choice2 = Choice.objects.create(choice_text="Erlang", question=self.question)

    def test_view(self):
        request = RequestFactory().get('/')
        request.user = self.user

        self.assertRaises(Http404, lambda: question(request, 42))

        response = question(request, self.question.id)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(200, response.status_code)




# Create your tests here.
