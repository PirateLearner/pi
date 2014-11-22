from django.conf import settings

BOOKMARK_FETCH_PRIORITY = getattr(settings, 'BOOKMARK_FETCH_PRIORITY', None)

