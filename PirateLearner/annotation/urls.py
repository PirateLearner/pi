from django.conf.urls import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from views.rest import UserViewSet, BlogContentViewSet, AnnotationViewSet, BlogContentCommentView, CurrentUserView, BlogParentViewSet

from rest_framework.urlpatterns import format_suffix_patterns

# Routers provide an easy way of automatically determining the URL conf.
'''
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'blogcontent', BlogContentViewSet)
'''

blogparent_list = BlogParentViewSet.as_view({
    'get': 'list'
})

blogparent_detail = BlogParentViewSet.as_view({
    'get': 'retrieve'
})

blogcontent_list = BlogContentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
blogcontent_detail = BlogContentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
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

urlpatterns = patterns('annotation.views',
    url(r'^post/ajax/$', 'annotations.post_annotation_ajax', name='annotation-post-comment-ajax'),
    url(r'^post/$',          'annotations.post_annotation',       name='annotation-post-comment'),
    url(r'^posted/$',        'annotations.annotation_done',       name='annotation-comment-done'),
    #url(r'^flag/(\d+)/$',    'moderation.flag',             name='comments-flag'),
    #url(r'^flagged/$',       'moderation.flag_done',        name='comments-flag-done'),
    url(r'^delete/(\d+)/$',  'moderation.delete',           name='annotation-delete'),
    url(r'^deleted/$',       'moderation.delete_done',      name='annotation-delete-done'),
    url(r'^approve/(\d+)/$', 'moderation.approve',          name='annotation-approve'),
    url(r'^approved/$',      'moderation.approve_done',     name='annotation-approve-done'),
    
    url(r'^blogparent/$', blogparent_list, name='blogparent-list'),
    url(r'^blogparent/(?P<pk>[0-9]+)/$', blogparent_detail, name='blogparent-detail'),
    url(r'^blogcontent/$', blogcontent_list, name='blogcontent-list'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/$', blogcontent_detail, name='blogcontent-detail'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/comments/$', BlogContentCommentView.as_view(), name='blogcontent-comments'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/current/$', CurrentUserView.as_view(), name='current-user'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^annotations/$', annotation_list, name='annotation-list'),
    url(r'^annotations/(?P<pk>[0-9]+)/$', annotation_detail, name='annotation-detail'),
    #url(r'^', include(router.urls)),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)

urlpatters = format_suffix_patterns(urlpatterns)