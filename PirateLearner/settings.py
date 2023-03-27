from PirateLearner.public_settings import *

DEBUG = True
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#Domain name
DOMAIN_URL = '//somethingnew.com/'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['somethingnew.com', '127.0.0.1']

SITE_ID = 1

# Example: "http://example.com/static/", "http://static.example.com/"
#STATIC_URL = '/static/'
STATIC_ROOT = '/home/web/piratelearner/static'
STATIC_URL = '/static/static/'

MEDIA_ROOT = '/home/web/piratelearner/media'
MEDIA_URL = '/static/media/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH+'/static/',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x4y7%ran4cc(p=(5s=d%nte&6=%sedhbmc28(2w902rtnvy@^s'

# List of callables that know how to import templates from various sources.


TEMPLATES = [
    { 
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
#                 'allauth.account.context_processors.account',
#                 'allauth.socialaccount.context_processors.socialaccount',
                'PirateLearner.context_processors.site_processor',
                'pl_messages.context_processor.notifications'

            ],
#             'loader': ['django.template.loaders.filesystem.Loader',
#                        'django.template.loaders.app_directories.Loader',
#                        'django.template.loaders.eggs.Loader'
#                        ],
            'debug': DEBUG,
        },
    },
]




DATABASES = {
    'default':
        {'ENGINE': 'django.db.backends.mysql', 'NAME': 'dbname', 'HOST': '127.0.0.1', 'USER': 'dbuser', 'PASSWORD': 'dbpassword', 'PORT': '3306'}
}

CKEDITOR_UPLOAD_PATH = 'images/'
CKEDITOR_CONFIGS = {
    'default': {                        
        'toolbar': [
                      ["Format", "Bold", "Italic", "Underline", "Strike", "Blockquote","Subscript", "Superscript", "SpellChecker"],
                      [ "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
                 'JustifyRight', 'JustifyBlock'],
                      ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink",'NumberedList', 'BulletedList', 'HorizontalRule', 'CreateDiv'], 
                      ['Undo', 'Redo'], ["Source", 'RemoveFormat','Iframe'],["Maximize"],['ShowBlocks', 'Syntaxhighlight', 'Mathjax'],
                     ],
        'contentsCss': STATIC_URL+'css/bootstrap.css',
    
        'codemirror' : {
                        # Set this to the theme you wish to use (codemirror themes)
                        'theme': 'default',
                        # Whether or not you want to show line numbers
                        'lineNumbers': 'true',
                        # Whether or not you want to use line wrapping
                        'lineWrapping': 'true',
                        # Whether or not you want to highlight matching braces
                        'matchBrackets': 'true',
                        # Whether or not you want tags to automatically close themselves
                        'autoCloseTags': 'false',
                        # Whether or not you want Brackets to automatically close themselves
                        'autoCloseBrackets': 'false',
                        # Whether or not to enable search tools, CTRL+F (Find), CTRL+SHIFT+F (Replace), CTRL+SHIFT+R (Replace All), CTRL+G (Find Next), CTRL+SHIFT+G (Find Previous)
                        'enableSearchTools': 'true',
                        # Whether or not you wish to enable code folding (requires 'lineNumbers' to be set to 'true')
                        'enableCodeFolding': 'true',
                        # Whether or not to enable code formatting
                        'enableCodeFormatting': 'false',
                        # Whether or not to automatically format code should be done when the editor is loaded
                        'autoFormatOnStart': 'false',
                        # Whether or not to automatically format code should be done every time the source view is opened
                        'autoFormatOnModeChange': 'false',
                        # Whether or not to automatically format code which has just been uncommented
                        'autoFormatOnUncomment': 'false',
                        # Define the language specific mode 'htmlmixed' for html including (css, xml, javascript), 'application/x-httpd-php' for php mode including html, or 'text/javascript' for using java script only
                        'mode': 'htmlmixed',
                        # Whether or not to show the search Code button on the toolbar
                        'showSearchButton': 'true',
                        # Whether or not to show Trailing Spaces
                        'showTrailingSpace': 'true',
                        # Whether or not to highlight all matches of current word/selection
                        'highlightMatches': 'true',
                        # Whether or not to show the format button on the toolbar
                        'showFormatButton': 'true',
                        # Whether or not to show the comment button on the toolbar
                        'showCommentButton': 'true',
                        # Whether or not to show the uncomment button on the toolbar
                        'showUncommentButton': 'true',
                        #Whether or not to show the showAutoCompleteButton button on the toolbar
                        'showAutoCompleteButton': 'true',
                        # Whether or not to highlight the currently active line
                        'styleActiveLine': 'true'
                        },
             
             'disallowedContent':{      
                        'p h1 h2 h3 h4 span blockquote':{
                                    #Disallow setting font-family or font-size
                                    'styles':['font*'],
                                },
                        },   

                
            'allowedContent':{
                        '*': {
                              
                              'attributes': ['id', 'itemprop', 'title', 'placeholder', 'type', 'data-*'],
                              'classes':['text-center', 'text-left', 'text-right', 'text-justify', 'center-text', 'text-muted', 
                                         'align-center', 'pull-left', 'pull-right', 'center-block', 'media', 'image',
                                         'list-unstyled', 'list-inline',
                                         'language-*', '*', 
                                        ],
                            },
                        'p': {
                                'attributes': ['id'],   
                            },
                        'h1 h2 h3 h4 em i b strong caption h5 h6 u s br hr': 'true',
                        'a': {
                                'attributes': ['!href','target','name', 'id', 'name', 'rel'],
                            },      
                        'img':{
                               #Do not allow image height and width styles
                               'attributes': ['!src', 'alt', 'id'],
                            },                        
                        'span ul ol li sup sub': 'true',
                        'div':{
                               'classes':'*',
                            },
                        'iframe':{
                                'classes':'*',
                                'attributes':'*',
                            },
                        'small abbr address footer section article dl dt dd kbd var samp form label input button textarea fieldset':'true',
                        'pre':{
                               'attributes': ['title'],
                               'classes':['*']
                            },
                        'code': 'true',
                        
                        'blockquote':'true',
                        'table':'true',
                        'tr':'true',
                        'th':'true',
                        'td':'true',
                        },
            'justifyClasses': ['text-left', 'text-center', 'text-right', 'text-justify'],
            'extraPlugins': 'button,toolbar,codesnippet,about,stylescombo,richcombo,floatpanel,panel,button,listblock,dialog,dialogui,syntaxhighlight,htmlwriter,removeformat,horizontalrule,widget,lineutils,mathjax,div,fakeobjects,iframe,image2,justify,blockquote,indent,indentlist,indentblock',
            'ignoreEmptyParagraph': 'true',   
            'coreStyles_bold': {
                            'element': 'b',
                            'overrides': 'strong',
                        },
            'coreStyles_italic':{
                            'element':'i',
                            'overrides':'em',
                        },
            #'fillEmptyBlocks':'false',#Might need a callback fn
            'image2_alignClasses':['pull-left','text-center','pull-right'],
            'mathJaxClass':'math-tex',
            'mathJaxLib':STATIC_URL+'js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
            'tabSpaces':'4',
            'indentClasses': ['col-xs-offset-1', 'col-xs-offset-2', 'col-xs-offset-3', 'col-xs-offset-4'],     
    },
    'author': {                        
        'toolbar': [
                      ["Format", "Bold", "Italic", "Underline", "Strike", "Blockquote","Subscript", "Superscript", "SpellChecker"],
                      [ "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
                 'JustifyRight', 'JustifyBlock'],
                      ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink",'NumberedList', 'BulletedList', 'HorizontalRule', 'CreateDiv'], 
                      ['Undo', 'Redo'], ["Source", 'RemoveFormat','Iframe'],["Maximize"],['ShowBlocks', 'Syntaxhighlight', 'Mathjax'],
                     ],
        'contentsCss': STATIC_URL+'css/bootstrap.css',
    
        'codemirror' : {
                        # Set this to the theme you wish to use (codemirror themes)
                        'theme': 'default',
                        # Whether or not you want to show line numbers
                        'lineNumbers': 'true',
                        # Whether or not you want to use line wrapping
                        'lineWrapping': 'true',
                        # Whether or not you want to highlight matching braces
                        'matchBrackets': 'true',
                        # Whether or not you want tags to automatically close themselves
                        'autoCloseTags': 'false',
                        # Whether or not you want Brackets to automatically close themselves
                        'autoCloseBrackets': 'false',
                        # Whether or not to enable search tools, CTRL+F (Find), CTRL+SHIFT+F (Replace), CTRL+SHIFT+R (Replace All), CTRL+G (Find Next), CTRL+SHIFT+G (Find Previous)
                        'enableSearchTools': 'true',
                        # Whether or not you wish to enable code folding (requires 'lineNumbers' to be set to 'true')
                        'enableCodeFolding': 'true',
                        # Whether or not to enable code formatting
                        'enableCodeFormatting': 'false',
                        # Whether or not to automatically format code should be done when the editor is loaded
                        'autoFormatOnStart': 'false',
                        # Whether or not to automatically format code should be done every time the source view is opened
                        'autoFormatOnModeChange': 'false',
                        # Whether or not to automatically format code which has just been uncommented
                        'autoFormatOnUncomment': 'false',
                        # Define the language specific mode 'htmlmixed' for html including (css, xml, javascript), 'application/x-httpd-php' for php mode including html, or 'text/javascript' for using java script only
                        'mode': 'htmlmixed',
                        # Whether or not to show the search Code button on the toolbar
                        'showSearchButton': 'true',
                        # Whether or not to show Trailing Spaces
                        'showTrailingSpace': 'true',
                        # Whether or not to highlight all matches of current word/selection
                        'highlightMatches': 'true',
                        # Whether or not to show the format button on the toolbar
                        'showFormatButton': 'true',
                        # Whether or not to show the comment button on the toolbar
                        'showCommentButton': 'true',
                        # Whether or not to show the uncomment button on the toolbar
                        'showUncommentButton': 'true',
                        #Whether or not to show the showAutoCompleteButton button on the toolbar
                        'showAutoCompleteButton': 'true',
                        # Whether or not to highlight the currently active line
                        'styleActiveLine': 'true'
                        },
             
             'disallowedContent':{      
                        'p h1 h2 h3 h4 span blockquote':{
                                    #Disallow setting font-family or font-size
                                    'styles':['font*'],
                                },
                        },   

                
            'allowedContent':{
                        '*': {
                              
                              'attributes': ['id', 'itemprop', 'title', 'placeholder', 'type', 'data-*'],
                              'classes':['text-center', 'text-left', 'text-right', 'text-justify', 'center-text', 'text-muted', 
                                         'align-center', 'pull-left', 'pull-right', 'center-block', 'media', 'image',
                                         'list-unstyled', 'list-inline',
                                         'language-*', '*', 
                                        ],
                            },
                        'p': {
                                'attributes': ['id'],   
                            },
                        'h1 h2 h3 h4 em i b strong caption h5 h6 u s br hr': 'true',
                        'a': {
                                'attributes': ['!href','target','name', 'id', 'name', 'rel'],
                            },      
                        'img':{
                               #Do not allow image height and width styles
                               'attributes': ['!src', 'alt', 'id'],
                            },                        
                        'span ul ol li sup sub': 'true',
                        'div':{
                               'classes':'*',
                            },
                        'iframe':{
                                'classes':'*',
                                'attributes':'*',
                            },
                        'small abbr address footer section article dl dt dd kbd var samp form label input button textarea fieldset':'true',
                        'pre':{
                               'attributes': ['title'],
                               'classes':['*']
                            },
                        'code': 'true',
                        
                        'blockquote':'true',
                        'table':'true',
                        'tr':'true',
                        'th':'true',
                        'td':'true',
                        },
            'justifyClasses': ['text-left', 'text-center', 'text-right', 'text-justify'],
            'extraPlugins': 'button,toolbar,codesnippet,about,stylescombo,richcombo,floatpanel,panel,button,listblock,dialog,dialogui,syntaxhighlight,htmlwriter,removeformat,horizontalrule,widget,lineutils,mathjax,div,fakeobjects,iframe,image2,justify,blockquote,indent,indentlist,indentblock',
            'ignoreEmptyParagraph': 'true',   
            'coreStyles_bold': {
                            'element': 'b',
                            'overrides': 'strong',
                        },
            'coreStyles_italic':{
                            'element':'i',
                            'overrides':'em',
                        },
            #'fillEmptyBlocks':'false',#Might netext-centerk fn
            'image2_alignClasses':['pull-left','text-center','pull-right'],
            'mathJaxClass':'math-tex',
            'mathJaxLib':STATIC_URL+'js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
            'tabSpaces':'4',
            'indentClasses': ['col-xs-offset-1', 'col-xs-offset-2', 'col-xs-offset-3', 'col-xs-offset-4'],     
    },
}
CKEDITOR_RESTRICT_BY_USER=True

DISQUS_API_KEY = 'QJezRiHWxv2FzzrMuOSvQPn99oil0LLyhZxdCAEd3s5cZTf6GUI5019NKznCEONu'
DISQUS_WEBSITE_SHORTNAME = 'piratelearner'

DEFAULT_FROM_EMAIL = 'you@somethingnew.com'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
EMAIL_SUBJECT_PREFIX = '[PirateLearner]'
EMAIL_HOST = 'smtp.webserver.com'
EMAIL_HOST_USER = 'pirate_learner_mailbox'
EMAIL_HOST_PASSWORD = 'password'
SERVER_EMAIL = 'you@somethingnew.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 25


MATHJAX_ENABLED=True
MATHJAX_LOCAL_PATH = 'js/MathJax/'
MATHJAX_CONFIG_FILE = "TeX-AMS-MML_HTMLorMML"
#MATHJAX_CONFIG_DATA = {
#    "tex2jax": {
#      "inlineMath":
#        [
#            ['$','$'],
#            ['\\(','\\)']
#        ]
#    }
#  }
MATHJAX_CONFIG_DATA = {
    "tex2jax": {
      "inlineMath":
        [
            ['$','$'],
            ['\\(','\\)']
        ],
       "displayMath": [ ['$$','$$'], ["\\[","\\]"] ],
       "processEscapes": True
    },
    "TeX": {
       "equationNumbers": {"autoNumber": "AMS"},
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

#blogging app settings
BLOGGING_MAX_ENTRY_PER_PAGE = 10

# ftech the bookmark from web pages depending upon the tags written for social networking sites

BOOKMARK_FETCH_PRIORITY = ['facebook','google','twitter','extra','None']
BOOKMARK_DEFAULT_IMAGE = DOMAIN_URL+STATIC_URL+'images/default_bookmark.jpg'

VOTING_ZERO_VOTES_ALLOWED = True

## Event Notification Settings

EVENTS_NOTIFICATIONS_LINK_PROTOCOL = "http"
EVENTS_NOTIFICATIONS_BACKENDS = [
                               ("email", "events.backends.email.EmailBackend"),
                               ]
