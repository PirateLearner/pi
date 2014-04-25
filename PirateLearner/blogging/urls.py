from django.conf.urls import patterns, url
import blogging.views as view


urlpatterns = patterns(
    '',
    url(r'^$', view.index, name='section-view'),
    url(r'^author/$', view.authors_list, name='author-list'),
    url(r'^author/(?P<slug>[\w.@+-]+)/(?P<post_id>\d+)$', view.author_post, name='author-posts'),
#    url(r'^feed/$', LatestEntriesFeed(), name='latest-posts-feed'),
    url(r'^(?P<year>\d{4})/$', view.archive, name='archive-year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', view.archive, name='archive-month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', view.archive, name='archive-day'),
#    url(r'^(?P<slug>[\w.+-/]+)/(?P<post_id>\d+)$', view.detail, name='post-detail'),
    url(r'^(?P<slug>[\w.+-/]+)/$', view.teaser, name='teaser-view'),
#    url(r'^(?P<slug>\D+)(?P<post_id>\d+)$', view.detail, name='post-detail'),
#    url(r'^(?P<path>\D*)$', view.teaser, name='teaser-view'),
#    url(r'^tag/$', TagsListView.as_view(), name='tag-list'),
#    url(r'^tag/(?P<tag>[-\w]+)/$', TaggedListView.as_view(), name='tagged-posts'),
#    url(r'^tag/(?P<tag>[-\w]+)/feed/$', TagFeed(), name='tagged-posts-feed'),
)

