
from django.conf.urls import patterns,url
from .views import *


urlpatterns = patterns("",
    url(r"^$", "spotlight.views.index", name="all_spotlight"),
    url(r"^featured/$", "spotlight.views.featured", name="featured_post"),
    url(r"^promoted/$", "spotlight.views.promoted", name="promoted_post"),
    url(r"^add/$", "spotlight.views.add_spotlight", name="add_spotlight"),
    url(r"^(\d+)/delete/$", "spotlight.views.delete_spotlight", name="delete_spotlight"),
    url(r'^tag/(?P<tag>[-\w]+)/$', "spotlight.views.tagged_spotlight", name='tagged-spotlight'),
)

