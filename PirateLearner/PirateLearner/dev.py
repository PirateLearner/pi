
# settings related to dev environment
DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = ''
STATIC_URL = '/static/static/'
MEDIA_ROOT = '/home/abhishek/git/PirateLearnerStatic/media'
MEDIA_URL = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/abhishek/git/PirateLearnerStatic/static',
)

DATABASES = {
    'default':{
    		'ENGINE': 'django.db.backends.mysql',
    		'NAME': 'sampledb',
    		'HOST': '127.0.0.1',
    		'USER': 'root',
    		'PASSWORD': 'root',
    		'PORT': '3306'
    }
}
