# settings specific to CMS APP

CMS_TEMPLATES = (
    ## Customize this
    ('page.html', 'Page'),
    ('feature.html', 'Page with Feature'),
    ('content_page.html', 'About Page'),
    ('content_page.html', 'Contact Us'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

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
