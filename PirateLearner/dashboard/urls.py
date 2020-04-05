<<<<<<< HEAD
__author__ = 'aquasan'

from django.conf.urls import include, url
from .views import *

app_name='dashboard'
=======
from django.urls import path, include, re_path
from .views import *

app_name="dashboard"
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62

urlpatterns = [

    path('',dashboard_home, name='dashboard-home'),
    re_path(r'^(?P<user_id>\d+)/profile/?$',dashboard_profile, name='dashboard-profile'),
    path('manage-articles/',manage_articles, name='dashboard-admin-articles'),
    path('published/',published_articles, name='dashboard-published'),
    path('pending/',pending_articles, name='dashboard-pending'),
    path('draft/',draft_articles, name='dashboard-draft'),
    path('bookmarks/',bookmark_articles, name='dashboard-bookmarks'),
    path('tag/add/', TagCreate.as_view(), name='tag-add'),
    re_path(r'tag/(?P<pk>[0-9]+)/$', TagUpdate.as_view(), name='tag-update'),
    re_path(r'tag/(?P<pk>[0-9]+)/delete/$', TagDelete.as_view(), name='tag-delete'),
    path('tags/', TagList.as_view(), name='tag-list'),
]



