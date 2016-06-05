from django.conf.urls import url

from .views import EventFilterView


urlpatterns = [
    url(r"^filters/$", EventFilterView.as_view(), name="notification_event_filters"),
]
