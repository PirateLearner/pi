__author__ = 'aquasan'

from django.conf.urls import patterns,url
from .views import *
urlpatterns = patterns('',
    url(r'^$',dashboard_home, name='dashboard'),
)



