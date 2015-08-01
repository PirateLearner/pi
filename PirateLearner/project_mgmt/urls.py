from django.conf.urls import patterns, url
import project_mgmt.views as view

urlpatterns = patterns(
    '',
    url(r'^$', view.index, name='wishlist-view'),
    )