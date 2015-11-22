__author__ = 'aquasan'

from django.conf.urls import patterns, include, url
from .views import *
urlpatterns = patterns('',

    url(r'^$',dashboard_home, name='dashboard-home'),
    url(r'^(?P<user_id>\d+)/profile/?$',dashboard_profile, name='dashboard-profile'),
    url(r'^manage-articles/?$',manage_articles, name='dashboard-admin-articles'),
    url(r'^published/?$',published_articles, name='dashboard-published'),
    url(r'^pending/?$',pending_articles, name='dashboard-pending'),
    url(r'^draft/?$',draft_articles, name='dashboard-draft'),
    url(r'^bookmarks/?$',bookmark_articles, name='dashboard-bookmarks'),
)



