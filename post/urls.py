from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<slug>\w+)/$', views.detail, name='detail'),  
    url(r'^create/$', views.create, name='create'),
    url(r'^api/$', views.api, name='api'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^delete/(?P<slug>\w+)/$', views.delete, name='delete'),
    url(r'^edit/(?P<slug>\w+)/$', views.edit, name='edit'),  
    url(r'^publish/(?P<slug>\w+)/$', views.publish, name='publish'),
    url(r'^comment/(?P<slug>\w+)/$', views.comment, name='comment'),
     
]