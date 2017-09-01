from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse

from .models import Question, Choice, Answer
from .views import QuestionView


class QuestionTest(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('test_user', 'test@gmail.com', 'test_user')

        self.question = Question.objects.create(question_text='Which programming language do you like the most?')
        self.choice1 = Choice.objects.create(choice_text="Python", question=self.question, pk=1)
        self.choice2 = Choice.objects.create(choice_text="Erlang", question=self.question, pk=2)

    def test_QuestionView(self):
        request = RequestFactory().get('/'+str(self.question.id)+'/')
        request.user = self.user
        # Fetch a non-existing question should raise 404
        self.assertRaises(Http404, lambda: QuestionView(request, 42))

        # The response of a normal existing question "GET" is an HttpResponse
        response = QuestionView(request, self.question.id)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(200, response.status_code)

        # Test an unauthorized user GET to '/question_id/' URL should be redirected to '/signup/'
        response = self.client.get(request.path, {})
        self.assertRedirects(response, '/signup/', 302, 200)

        loggedIn = self.client.login(username='test_user', password='test_user')
        # User should be loggedIn "I know it is not related to test it here but I did it for the test flow"
        self.assertEqual(True, loggedIn)

        # A User POST selecting choice '1' should result in a redirect to the next question
        response = self.client.post(request.path, {'option': 1})
        self.assertEqual(302, response.status_code)
        self.assertNotEqual(request.path, response.url)

        # A user POST request with no choice selected should result in a redirect to the same URL
        response = self.client.post(request.path, {})
        self.assertEqual(302, response.status_code)
        self.assertEqual(request.path, response.url)

class IndexTest(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('test_user', 'test@gmail.com', 'test_user')

        # Here I should've used fixtures
        self.question1 = Question.objects.create(question_text='Which programming language do you like the most?')
        self.choice1 = Choice.objects.create(choice_text="Python", question=self.question1)
        self.choice2 = Choice.objects.create(choice_text="Erlang", question=self.question1)
        #
        self.question2 = Question.objects.create(question_text='some question?')
        self.choice3 = Choice.objects.create(choice_text="Python", question=self.question2)
        self.choice4 = Choice.objects.create(choice_text="Erlang", question=self.question2)

    def test_IndexView(self):
        request = RequestFactory().get('/')
        request.user = self.user

        # Test an unauthorized user GET to '/question_id/' URL should be redirected to '/signup/'
        response = self.client.get(request.path, {})
        self.assertRedirects(response, '/signup/', 302, 200)

        loggedIn = self.client.login(username='test_user', password='test_user')
        self.assertEqual(True, loggedIn)

        # An authorized user request to '/question/' or '/' should be redirected to a '/question_id/'
        response = self.client.get(request.path, {})
        self.assertEqual(302, response.status_code)
        self.assertNotEqual('/signup/', response.url)

        # Append an answer
        self.answer = Answer.objects.create(choice=self.choice1, user=request.user)
        # The request should be redirected to  '/question_id/'
        response = self.client.get(request.path, {})
        self.assertEqual(302, response.status_code)
        self.assertNotEqual('/signup/', response.url)
        # Append a new Answer (now all questions are answered)
        self.answer2 = Answer.objects.create(choice=self.choice3, user=request.user)
        # The request should return HttpResponse (done.html)
        response = self.client.get(request.path, {})
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(200, response.status_code)

class SignUpTest(TestCase):
    pass