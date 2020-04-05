
import base64

from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language, activate
from six import python_2_unicode_compatible
from six.moves import cPickle as pickle  # pylint: disable-msg=F
import six
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from events.compat import GenericForeignKey
from events.conf import settings

from events.utils import load_media_defaults, event_filter_for_user


EVENT_MEDIA, EVENT_MEDIA_DEFAULTS = load_media_defaults()

class InvalidEvent(Exception):
    """ Easy to understand naming conventions work best! """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{0} does not exist in EventType! please create it first.".format(repr(self.value))

@python_2_unicode_compatible
class EventType(models.Model):

    label = models.CharField(_("label"), max_length=40)
    display = models.CharField(_("display"), max_length=50)
    description = models.CharField(_("description"), max_length=100)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _("event type")
        verbose_name_plural = _("event types")

    @classmethod
    def create(cls, label, display, description, verbosity=1):
        """
        Creates a new EventType.

        This is intended to be used by other apps as a post_syncdb manangement step.
        """
        try:
            event_type = cls._default_manager.get(label=label)
            updated = False
            if display != event_type.display:
                event_type.display = display
                updated = True
            if description != event_type.description:
                event_type.description = description
                updated = True
            if updated:
                event_type.save()
                if verbosity > 1:
                    print(("Updated %s EventType" % label))
        except cls.DoesNotExist:
            cls(label=label, display=display, description=description).save()
            if verbosity > 1:
                print(("Created %s EventType" % label))


class EventFilter(models.Model):
    """
    Indicates, for a given user, whether to deny action of a given type to a given action.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"),on_delete = models.CASCADE)
    event_type = models.ForeignKey(EventType, verbose_name=_("notice type"),on_delete = models.CASCADE)
    action = models.CharField(_("action"), max_length=10, choices=EVENT_MEDIA)
    scoping_content_type = models.ForeignKey(ContentType, null=True, blank=True,on_delete = models.SET_NULL)
    scoping_object_id = models.PositiveIntegerField(null=True, blank=True)
    scoping = GenericForeignKey("scoping_content_type", "scoping_object_id")

    @classmethod
    def for_user(cls, user, notice_type, medium, scoping=None):
        """
        Kept for backwards compatibilty but isn't used anywhere within this app

        @@@ consider deprecating
        """
        return event_filter_for_user(user, notice_type, medium, scoping)

    class Meta:
        verbose_name = _("event filter")
        verbose_name_plural = _("event filters")
        unique_together = ("user", "event_type", "action", "scoping_content_type", "scoping_object_id")


class EventQueueBatch(models.Model):
    """
    A queued notice.
    Denormalized data for a notice.
    """
    pickled_data = models.TextField()


def send(to, label, sender=None, **kwargs):
    """
    Creates a new notification.

    This is intended to be how other apps create new notification.

    notification.send(user, "friends_invite_sent", {
        "spam": "eggs",
        "foo": "bar",
    )
    1. get all user from given gruop if to is str object;
        otherwise to is a list of users objects
    @todo

    2. via field indicates the backend which will be used to send the Notifications.
        It should be one of the EVENTS_NOTIFICATIONS_BACKENDS defined in settings.
        If it is not a list of strings convert it to one.

    """
    sent = False

    extra_context = kwargs.get("extra_context",{})
    scoping = kwargs.get("scoping",None)
    notice_type = EventType.objects.get(label=label)

    users = to
    if isinstance(to, six.string_types):
        users = User.objects.filter(groups__name=to)


    for user in users:
        for backend in list(settings.EVENTS_NOTIFICATIONS_BACKENDS.values()):
            if backend.can_send(user, notice_type, scoping=scoping):
                backend.deliver(user, sender, notice_type, **kwargs)
                sent = True
    return sent


def queue(to, label, extra_context=None, sender=None, template=None):
    """
    Queue the notification in EventQueueBatch. This allows for large amounts
    of user notifications to be deferred to a seperate process running outside
    the webserver.
    extract pk if to is queryset; extract user.pk after getting all user from given gruop if to is str object;
    otherwise to is a list of users objects, extract user.pk
    """
    if extra_context is None:
        extra_context = {}
    if isinstance(to, QuerySet):
        users = [row["pk"] for row in to.values("pk")]
    elif isinstance(to, six.string_types):
        users = User.objects.filter(groups__name=to)
        users = [user.pk for user in users]
    else:
        users = [user.pk for user in to]
    notices = []
    for user in users:
        notices.append((user, label, extra_context, sender))
    EventQueueBatch(pickled_data=base64.b64encode(pickle.dumps(notices))).save()

