import os
gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
# Django settings for PirateLearner project.



ADMINS = (
    # ('Your Name', 'your_email@example.com'),
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

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x1y3%ran2cc(s=(5p=d%noe&6=%sedhbmc28(2w902rtnvy@^s'

# List of callables that know how to import templates from various sources.




ROOT_URLCONF = 'PirateLearner.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'PirateLearner.wsgi.application'





SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


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
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.stackexchange',
    'allauth.socialaccount.providers.twitter',
    'blogging',
    'ckeditor',
    'disqus',

)

LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

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


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)

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





