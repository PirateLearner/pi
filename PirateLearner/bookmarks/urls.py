
from django.conf.urls import patterns,url
from .views import *


urlpatterns = patterns("",
    url(r"^$", "bookmarks.views.bookmarks", name="all_bookmarks"),
    url(r"^your_bookmarks/$", "bookmarks.views.your_bookmarks", name="your_bookmarks"),
    url(r"^add/$", "bookmarks.views.add", name="add_bookmark"),
    url(r'^add-model/(?P<model_name>[\w.+-/]+)/$', "bookmarks.views.add_folder", name='add-model-folder'),
    url(r"^\w*/?(\d+)/update/$", "bookmarks.views.update", name="update_bookmark_instance"),
    url(r'^tag/(?P<tag>[-\w]+)/$', "bookmarks.views.tagged_bookmarks", name='tagged-bookmarks'),
    url(r'^(?P<slug>[\w.+-/]+)/$', "bookmarks.views.bookmark_details", name='detail-view'),
)

