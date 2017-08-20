from django.contrib.auth.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^(?P<username>\w+)/image/$', views.image_profile, name='image_profile'),
    url(r'^(?P<username>\w+)/posts/$', views.list_posts, name='list_posts'), 
]
