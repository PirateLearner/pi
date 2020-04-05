from django.conf.urls import patterns, url
import project_mgmt.views as view

app_name="project_mgmt"

urlpatterns = [
    '',
    url(r'^$', view.index, name='wishlist-view'),
    ]