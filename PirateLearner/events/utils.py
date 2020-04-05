from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from events.conf import settings


def load_media_defaults():
    media = []
    defaults = {}
    for key, backend in list(settings.EVENTS_NOTIFICATIONS_BACKENDS.items()):
        # key is a tuple (action_id, backend_label)
        media.append(key)
        defaults[key[0]] = backend.spam_sensitivity
    return media, defaults

def event_filter_for_user(user, event_type, action, scoping=None):
    """
    candidate for overriding via a hookset method so you can customize lookup at site level
    return None if no such filter is found or else return the filters
    """
    kwargs = {
        "event_type": event_type,
        "action": action
    }
    if scoping:
        kwargs.update({
            "scoping_content_type": ContentType.objects.get_for_model(scoping),
            "scoping_object_id": scoping.pk
        })
    else:
        kwargs.update({
            "scoping_content_type__isnull": True,
            "scoping_object_id__isnull": True
        })
    try:
        return user.eventfilter_set.get(**kwargs)
    except ObjectDoesNotExist:
        return None

def create_filter_for_user(user, event_type, action, scoping=None):
    '''
    @note: use to create the deny filter for user
    '''
    kwargs = {
        "event_type": event_type,
        "action": action
    }
    if scoping:
        kwargs.update({
            "scoping_content_type": ContentType.objects.get_for_model(scoping),
            "scoping_object_id": scoping.pk
        })
    else:
        kwargs.update({
            "scoping_content_type": None,
            "scoping_object_id": None
        })
        setting = user.eventfilter_set.create(**kwargs)
        return setting    

def is_broadcast(user):
    if user and user.is_staff:
        return True
    else:
        return False


  
# def broadcast(to,sender,subject,body):
#     if is_broadcast(sender):
#         default_http_protocol = getattr(settings, "EVENT_LINK_PROTOCOL", "http")
#         current_site = Site.objects.get_current()
#         base_url = "{0}://{1}".format(default_http_protocol, current_site.domain)
#         context = Context({
#             "default_http_protocol": default_http_protocol,
#             "current_site": current_site,
#             "base_url": base_url
#         })
#         sender = sender.email        
#         extra_context = kwargs.get('extra_context',None)
#         if extra_context:
#             context.update(extra_context)
#         users = User.objects.filter(groups__name=to)
# 
#         context.update({
#             "recipient": recipient,
#             "sender": sender,
#             "notice": ugettext(notice_type.display),
#         })
        
