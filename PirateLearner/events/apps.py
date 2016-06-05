from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "events"
    label = "events_notifications"
    verbose_name = _("Event Notifications")
