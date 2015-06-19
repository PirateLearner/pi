from django.conf.urls import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from views import api_root

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('rest.views',
    url(r'^$', api_root),
    url(r'^annotation/', include('annotation.urls', namespace='annotation')),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)

urlpatters = format_suffix_patterns(urlpatterns)