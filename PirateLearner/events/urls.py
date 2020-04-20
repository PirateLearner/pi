from django.conf.urls import url

from events.views import EventFilterView

app_name="events"

urlpatterns = [
    url(r"^filters/$", EventFilterView.as_view(), name="notification_event_filters"),
]
