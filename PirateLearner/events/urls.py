from django.conf.urls import url

from events.views import EventFilterView

<<<<<<< HEAD
app_name='events'
=======
app_name="events"
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62

urlpatterns = [
    url(r"^filters/$", EventFilterView.as_view(), name="notification_event_filters"),
]
