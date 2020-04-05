
<<<<<<< HEAD
from django.conf.urls import url
from .views import *

app_name = 'bookmarks'
=======
from django.urls import path, include, re_path
from .views import *

app_name="bookmarks"
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62

urlpatterns = [
    path("", bookmarks, name="all_bookmarks"),
    path("your_bookmarks/", your_bookmarks, name="your_bookmarks"),
    path("add/", add, name="add_bookmark"),
    re_path(r'^add-model/(?P<model_name>[\w.+-/]+)/$', add_folder, name='add-model-folder'),
#     path("\w*/?(\d+)/update/$", "bookmarks.views.update", name="update_bookmark_instance"),
    re_path(r'^update/(?P<bookmark_instance_id>\d+)/$', update, name='update_bookmark_instance'),
    path('manage/', manage, name='manage_bookmarks'),
    path('snippet/', snippet_testing, name='snippet_test'),
    re_path(r'^tag/(?P<tag>[-\w]+)/$', tagged_bookmarks, name='tagged-bookmarks'),
    re_path(r'^(?P<slug>[\w.+-/]+)/$', bookmark_details, name='detail-view'),
#     path('api/?$)/$', BookmarkList.as_view(), name='api-list'),
]

