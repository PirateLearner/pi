
from django.conf.urls import patterns,url
from .views import *


urlpatterns = [
    url(r"^$", bookmarks, name="all_bookmarks"),
    url(r"^your_bookmarks/$", your_bookmarks, name="your_bookmarks"),
    url(r"^add/$", add, name="add_bookmark"),
    url(r'^add-model/(?P<model_name>[\w.+-/]+)/$', add_folder, name='add-model-folder'),
#     url(r"^\w*/?(\d+)/update/$", "bookmarks.views.update", name="update_bookmark_instance"),
    url(r'^update/(?P<bookmark_instance_id>\d+)/$', update, name='update_bookmark_instance'),
    url(r'^manage/$', manage, name='manage_bookmarks'),
    url(r'^tag/(?P<tag>[-\w]+)/$', tagged_bookmarks, name='tagged-bookmarks'),
    url(r'^(?P<slug>[\w.+-/]+)/$', bookmark_details, name='detail-view'),
#     url(r'^api/?$)/$', BookmarkList.as_view(), name='api-list'),
]

