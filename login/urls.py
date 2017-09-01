from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'question'

urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.QuestionView, name='question'),
]
