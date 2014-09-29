import os
gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ABSOLUTE_PATH = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
# Django settings for PirateLearner project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
     ('Abhishek Rai', 'abnith.rai812@gmail.com'),
     ('Anshul Thakur','anshulthakurjourneyendless@gmail.com'),
     ('Captain','captain@piratelearner.com')
)

MANAGERS = ADMINS



# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['piratelocal.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
#STATIC_URL = '/static/'
STATIC_ROOT = '/home/craft/git/PirateLearnerStatic/static/'
STATIC_URL = '/static/static/'

MEDIA_ROOT = '/home/craft/git/PirateLearnerStatic/media'
MEDIA_URL = '/media/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x1y3%ran2cc(s=(5p=d%noe&6=%sedhbmc28(2w902rtnvy@^s'

# List of callables that know how to import templates from various sources.




ROOT_URLCONF = 'PirateLearner.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'PirateLearner.wsgi.application'





SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = (
#    os.path.join(PROJECT_PATH, 'static'),
#)

SITE_ID = 1

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.transaction.TransactionMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

INSTALLED_APPS = (
    'djangocms_admin_style',
    'djangocms_text_ckeditor',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'reversion',
#    'aldryn_blog',
#    'aldryn_common',
    'django_select2',
    'easy_thumbnails',
    'filer',
    'taggit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
#     'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
#     'allauth.socialaccount.providers.linkedin',
#     'allauth.socialaccount.providers.linkedin_oauth2',
#     'allauth.socialaccount.providers.stackexchange',
    'allauth.socialaccount.providers.twitter',
    'crispy_forms',
    'blogging',
    'annotation',
    'ckeditor',
    'disqus',
    'dashboard',

    'pl_messages',
    'rest_framework',
    'meta_tags',
    'project_mgmt',
#     'django_mathjax',
)

LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
)

CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'hide_untranslated': False,
        'redirect_on_fallback': True,
        'public': True,
    },
    1: [
        {
            'redirect_on_fallback': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'public': True,
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('page.html', 'Page'),
    ('feature.html', 'Page with Feature'),
    ('content_page.html', 'About Page'),
    ('content_page.html', 'Contact Us'),
)

# allauth related settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)

LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}



CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATABASES = {
    'default':
        {'ENGINE': 'django.db.backends.mysql', 'NAME': 'sampledb', 'HOST': '127.0.0.1', 'USER': 'root', 'PASSWORD': 'root', 'PORT': '3306'}
}
# default is 10 px
MPTT_ADMIN_LEVEL_INDENT = 20
SOUTH_MIGRATION_MODULES = {
        'easy_thumbnails': 'easy_thumbnails.south_migrations',
	'taggit': 'taggit.south_migrations',
    }



THUMBNAIL_ALIASES = {
    '': {
        'teaser': {'size': (50, 50), 'crop': True},
    },
}
CKEDITOR_UPLOAD_PATH = 'images/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'justifyClasses': [ 'AlignLeft', 'AlignCenter', 'AlignRight', 'AlignJustify' ],
    },
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

DISQUS_API_KEY = 'QJezRiHWxv2FzzrMuOSvQPn99oil0LLyhZxdCAEd3s5cZTf6GUI5019NKznCEONu'
DISQUS_WEBSITE_SHORTNAME = 'piratelocal'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
EMAIL_SUBJECT_PREFIX = '[PirateLearner]'


MATHJAX_ENABLED=True
MATHJAX_LOCAL_PATH = 'js/MathJax/'
MATHJAX_CONFIG_FILE = "TeX-AMS-MML_HTMLorMML"
MATHJAX_CONFIG_DATA = {
    "tex2jax": {
      "inlineMath":
        [
            ['$','$'],
            ['\\(','\\)']
        ]
    }
  }

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


META_SITE_PROTOCOL = 'http'
# META_SITE_DOMAIN = 'pirateLearner.com' using META_USE_SITE SETTING
META_SITE_TYPE = 'article' # override when passed in __init__
META_SITE_NAME = 'Pirate Learner'
#META_INCLUDE_KEYWORDS = [] # keyword will be included in every article
#META_DEFAULT_KEYWORDS = [] # default when no keyword is provided in __init__
#META_IMAGE_URL = '' # Use STATIC_URL 
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
META_USE_SITES = True
META_PUBLISHER_FB_ID = 'https://www.facebook.com/PirateLearner' # can use PAGE URL or Publisher id ID
META_PUBLISHER_GOOGLE_ID = 'https://plus.google.com/116465481265465787624' # Google+ ID 
META_FB_APP_ID = ''

