__author__ = 'aquasan'
from django import template
from ..models import ParticipantNotifications
register = template.Library()

@register.simple_tag
def get_message_count(user, thread):
    notification = ParticipantNotifications.objects.filter(participant=user, thread=thread)
    if notification:
        notification = notification.get()
    else:
        return 0
    return notification.message_count

@register.simple_tag
def get_class(user, thread):
    if get_message_count(user, thread):
        return 'unread'
    return ''

@register.assignment_tag
def get_user(user, thread):
    participants = thread.participants.all()
    for u in participants:
        if u != user:
            return u
    return user