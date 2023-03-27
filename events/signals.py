import django.dispatch


generate_event = django.dispatch.Signal(
    #providing_args=["event_label", "user", "source_content_type", "source_object_id"]
)

