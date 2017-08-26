from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=100, default='test')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length=20, default='UNKNOWN')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "[+] "+ self.choice_text

class Answer(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "User: " + self.user.username + ", Question: " + self.choice.question.question_text + ", Answer: " + self.choice.choice_text