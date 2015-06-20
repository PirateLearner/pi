from django.conf import settings

BOOKMARK_FETCH_PRIORITY = getattr(settings, 'BOOKMARK_FETCH_PRIORITY', None)
BOOKMARK_DEFAULT_IMAGE = getattr(settings, 'BOOKMARK_DEFAULT_IMAGE', None)

