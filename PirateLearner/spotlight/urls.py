
<<<<<<< HEAD
from django.conf.urls import url
from .views import *

app_name='spotlight'
=======
from django.urls import path, re_path
from .views import *

app_name="spotlight"
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62

urlpatterns = [
    path("", index, name="all_spotlight"),
    path("featured/", featured, name="featured_post"),
    path("promoted/", promoted, name="promoted_post"),
    path("add/", add_spotlight, name="add_spotlight"),
    re_path(r"^(\d+)/delete/$", delete_spotlight, name="delete_spotlight"),
    re_path(r'^tag/(?P<tag>[-\w]+)/$', tagged_spotlight, name='tagged-spotlight'),
]

