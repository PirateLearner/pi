__author__ = 'aquasan'

from django.conf.urls import patterns
from django.urls import re_path as url
from .views import *
urlpatterns = patterns('',
    url(r'^$',details, name='cms_home'),
    url(r'^page_create/$',page_create, name='cms_page_create')
)



