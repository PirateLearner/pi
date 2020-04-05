
from django.conf.urls import url
from .views import *

app_name='spotlight'

urlpatterns = [
    url(r"^$", index, name="all_spotlight"),
    url(r"^featured/$", featured, name="featured_post"),
    url(r"^promoted/$", promoted, name="promoted_post"),
    url(r"^add/$", add_spotlight, name="add_spotlight"),
    url(r"^(\d+)/delete/$", delete_spotlight, name="delete_spotlight"),
    url(r'^tag/(?P<tag>[-\w]+)/$', tagged_spotlight, name='tagged-spotlight'),
]

