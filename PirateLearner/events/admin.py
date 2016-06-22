from django.contrib import admin
from events.models import EventType, EventQueueBatch, EventFilter

# Register your models here.

admin.site.register(EventType)
admin.site.register(EventFilter)
admin.site.register(EventQueueBatch)