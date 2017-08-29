from django.conf.urls import url, include
from django.contrib import admin
from login import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^question/', include('login.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^error/$', views.error, name='error'),
    url(r'^login/$', views.login_view, name='login'),
]
