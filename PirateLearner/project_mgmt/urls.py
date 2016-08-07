from django.conf.urls import patterns, url
import project_mgmt.views as view

urlpatterns = [
    '',
    url(r'^$', view.index, name='wishlist-view'),
    ]