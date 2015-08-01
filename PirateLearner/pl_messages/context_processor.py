__author__ = 'aquasan'
from .models import get_user_notifications, get_notification_count
from django.contrib.auth.models import User


def notifications(request):
    try:
        user = request.user
    except User.DoesNotExist:
        user = None
    if user is not None:
        return {
            'notifications': get_user_notifications(user),
            'notification_count': get_notification_count(user)
        }
    return {}