from django.conf.urls import patterns, include
from annotations import views
from django.urls import re_path as url

from rest_framework.urlpatterns import format_suffix_patterns

app_name="annotations"
'''
from annotations.views import (
           BlogContentViewSet, UserViewSet, AnnotationViewSet,
           BlogContentCommentView, CurrentUserView,
           api_root)

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

annotation_list = AnnotationViewSet.as_view({
    'get': 'list',
    'post': 'create'
    })
annotation_detail = AnnotationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
    })


urlpatterns = patterns('',
    url(r'^blogcontent/$', blogcontent_list, name='blogcontent-list'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/$', blogcontent_detail, name='blogcontent-detail'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/comments/$', BlogContentCommentView.as_view(), name='blogcontent-comments'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/current/$', CurrentUserView.as_view(), name='current-user'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    #url(r'^annotations/$', views.AnnotationViewList.as_view(), name='annotations-list'),
    url(r'^annotations/$', annotation_list, name='annotations-list'),
    #url(r'^annotations/(?P<pk>[0-9]+)/$', views.AnnotationViewDetail.as_view(), name='annotations-detail'),
    url(r'^annotations/(?P<pk>[0-9]+)/$', annotation_detail, name='annotations-detail'),
    url(r'^rest/$', api_root),
#   url(r'^$', views.home, name='home'),
#    url(r'^/(?P<id>\d+)/', views.update, name='update')
 )
urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
urlpatters = format_suffix_patterns(urlpatterns)
'''