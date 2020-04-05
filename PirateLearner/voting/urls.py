'''
Created on 07-May-2015

@author: craft
'''
from django.conf.urls import patterns, url, include
from voting import views

from rest_framework.urlpatterns import format_suffix_patterns

app_name="voting"

'''
from voting.views import (
           BlogContentViewSet, UserViewSet, VoteViewSet,
           BlogContentVoteView, CurrentUserView,
           api_root, VoteList, VoteDetail)

blogcontent_list = BlogContentViewSet.as_view({
    'get': 'list'
    })
blogcontent_detail = BlogContentViewSet.as_view({
    'get': 'retrieve',
    })

user_list = UserViewSet.as_view({
    'get': 'list'
    })
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
    })

"""
vote_list = VoteViewSet.as_view({
    'get': 'list',
    'post': 'create'
    })
vote_detail = VoteViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
    })
"""
vote_list = VoteList.as_view()
vote_detail = VoteDetail.as_view()

urlpatterns = patterns('',
    url(r'^blogcontent/$', blogcontent_list, name='blogcontent-list'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/$', blogcontent_detail, name='blogcontent-detail'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/comments/$', BlogContentVoteView.as_view(), name='blogcontent-comments'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/current/$', CurrentUserView.as_view(), name='current-user'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    #url(r'^annotations/$', views.AnnotationViewList.as_view(), name='annotation-list'),
    url(r'^votes/$', vote_list, name='vote-list'),
    #url(r'^annotations/(?P<pk>[0-9]+)/$', views.AnnotationViewDetail.as_view(), name='annotation-detail'),
    url(r'^votes/(?P<pk>[0-9]+)/$', vote_detail, name='vote-detail'),
    url(r'^rest/$', api_root),
#   url(r'^$', views.home, name='home'),
#    url(r'^/(?P<id>\d+)/', views.update, name='update')
 )
urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
urlpatterns = format_suffix_patterns(urlpatterns)
'''