from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    
    url(r'^create/$', views.create_or_edit_post, name='create'),
    #url(r'^load/$', views.load_post, name='load_post'),
    
    url(r'^edit/(?P<slug>[-\w]+)/$', views.create_or_edit_post, name='edit'),  
    url(r'^draft/$', views.draft_or_publish_post, name='draft_post'),
    url(r'^publish/$', views.draft_or_publish_post, name='publish_post'),
    
    url(r'^upload/$', views.image_upload, name='image_upload'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^(?P<slug>[-\w]+)/$', views.detail, name='detail'),     
    
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete, name='delete'),

    url(r'^publish/(?P<slug>[-\w]+)/$', views.publish, name='publish'),
    url(r'^comment/(?P<slug>[-\w]+)/$', views.comment, name='comment'),
     
]