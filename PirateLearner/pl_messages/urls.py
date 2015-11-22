__author__ = 'aquasan'

from django.conf.urls import patterns, include, url
from .views import *
urlpatterns = patterns('',
    url(r'^$', home, name='home_message'),
    url(r'^compose/$', new_message, name='new_message'),
    url(r'^all/$', home, name='all_threads'),
    url(r'^save/$', save_message, name='save_message'),
    url(r'^thread/view/([0-9]+)$', thread_messages, name='thread_messages'),

)
