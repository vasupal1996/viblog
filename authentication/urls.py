from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^username/$', views.check_username, name='username'),
    url(r'^email/$', views.check_email, name='email'),
]