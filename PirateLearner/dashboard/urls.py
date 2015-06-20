__author__ = 'aquasan'

from django.conf.urls import patterns,url
from .views import *
urlpatterns = patterns('',
    url(r'^$',dashboard_home, name='dashboard-home'),
    url(r'^(?P<user_id>\d+)/profile/$',dashboard_profile, name='dashboard-profile'),
)



