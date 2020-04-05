from django.urls import path, re_path

import blogging.views as view
from blogging.forms import *

app_name="blogging"

urlpatterns = [
    path('', view.index, name='section-view'),
    path('testing/',view.testCase,name='migrate-db'),
    path('contact/', view.ContactUs, name='contact-us'),
    path('create-post/', view.new_post, name='create-post'),
    re_path(r'^edit-post/(?P<post_id>\d+)/$', view.edit_post, name='edit-post'),
    re_path(r'^edit-section/(?P<section_id>\d+)/$', view.edit_section, name='edit-section'),
#    path('create-content/', view.ContentWizard.as_view([ContentTypeForm, ContentForm])),
    path('content-type/', view.content_type, name='content-type'),
    path('get-index/', view.BuildIndex, name='build-index'),
    re_path(r'^add-model/(?P<model_name>[\w.+-/]+)/$', view.add_new_model, name='add-model-content-type'),
    path('author/', view.authors_list, name='author-list'),
    re_path(r'^author/(?P<slug>[\w.@+-]+)/(?P<post_id>\d+)$', view.author_post, name='author-posts'),
#   path('feed/', LatestEntriesFeed(), name='latest-posts-feed'),
    re_path(r'^(?P<year>\d{4})/$', view.archive, name='archive-year'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', view.archive, name='archive-month'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', view.archive, name='archive-day'),
#    re_path(r'^(?P<slug>[\w.+-/]+)/(?P<post_id>\d+)$', view.detail, name='post-detail'),
    re_path(r'^tag/(?P<tag>[-\w]+)/$', view.tagged_post, name='tagged-posts'),
    path('manage/', view.manage , name='manage_articles'),
    re_path(r'^(?P<slug>[\w.+-/]+)/$', view.teaser, name='teaser-view'),
#    re_path(r'^(?P<slug>\D+)(?P<post_id>\d+)$', view.detail, name='post-detail'),
#    re_path(r'^(?P<path>\D*)$', view.teaser, name='teaser-view'),
#    path('tag/', TagsListView.as_view(), name='tag-list'),

#    re_path(r'^tag/(?P<tag>[-\w]+)/feed/$', TagFeed(), name='tagged-posts-feed'),
]
