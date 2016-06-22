from django.template import Context
from django.template.loader import render_to_string

from django.contrib.sites.models import Site

from events.conf import settings
from events.utils import event_filter_for_user


class BaseBackend(object):
    """
    The base backend.
    """
    def __init__(self, medium_id, spam_sensitivity=None):
        self.medium_id = medium_id
        if spam_sensitivity is not None:
            self.spam_sensitivity = spam_sensitivity

    def can_send(self, user, notice_type, scoping):
        """
        Determines whether this backend is allowed to send a notification to
        the given user and notice_type.
        """
        return bool(event_filter_for_user(user, notice_type, self.medium_id, scoping) is None)

    def deliver(self, recipient, sender, notice_type, **kwargs):
        """
        Deliver a notification to the given recipient.
        """
        raise NotImplementedError()

    def get_formatted_messages(self, formats, label, context):
        """
        Returns a dictionary with the format identifier as the key. The values are
        are fully rendered templates with the given context.
        """
        format_templates = {}
        for fmt in formats:
            # conditionally turn off autoescaping for .txt extensions in format
            ## for now we are not using the labels
            if fmt.endswith(".txt"):
                context.autoescape = False
            format_templates[fmt] = render_to_string(
               # "pinax/notifications/{0}/{1}".format(label, fmt),
                "events/notifications/{0}".format(fmt), context)
        return format_templates

    def default_context(self):
        '''
        @todo: change the setting variables
        '''
        default_http_protocol = getattr(settings, "EVENTS_NOTIFICATIONS_LINK_PROTOCOL", "http")
        current_site = Site.objects.get_current()
        base_url = "{0}://{1}".format(default_http_protocol, current_site.domain)
        return Context({
            "default_http_protocol": default_http_protocol,
            "current_site": current_site,
            "base_url": base_url
        })
