from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views

from authentication.views import register
from activity.views import get_dislike, get_like, user_activity

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^draceditor/', include('draceditor.urls')),
    # url(r'^api/', include('activity.urls', namespace='meta')),

    url(r'^login/$', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', register, name='register'),
    #url(r'^', include('post.urls', namespace='post')),

    url(r'^activity/like/$', get_like, name='get_like'),
    url(r'^activity/dislike/$', get_dislike, name='get_dislike'),
    url(r'^activity/user/$', user_activity, name='user_activity'),

    url(r'^settings/', include('core.urls', namespace='core')),
    url(r'^check/', include('authentication.urls', namespace='check')),
    url(r'^', include('post.urls', namespace='post')),

 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)