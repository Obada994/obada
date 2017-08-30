from django.conf.urls import url, include
from django.contrib import admin
from login import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users-api', views.UserViewSet.as_view())
# router.register(r'questions-api', views.QuestionViewSet.as_view())

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^question/', include('login.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^error/$', views.error, name='error'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^rest/', views.AnsweresList.as_view()),

]

# urlpatterns = format_suffix_patterns(urlpatterns)