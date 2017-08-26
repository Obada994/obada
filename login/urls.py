from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^(\d+)/(\d+)$', views.choice, name='choice'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
]
