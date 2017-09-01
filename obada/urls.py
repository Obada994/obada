from django.conf.urls import url, include
from django.contrib import admin
from login import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'all_users_readOnly', views.UserViewSet, base_name='user')
router.register(r'all_answers_readOnly', views.AnswerViewSet)
router.register(r'all_questions_readOnly', views.QuestionViewSet)


urlpatterns = [
    url(r'^', include('login.urls'), name='question'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'signup'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^question/', include('login.urls')),
    url(r'api/', include(router.urls)),
    url(r'myAnswers/', views.UserAnswers),

]