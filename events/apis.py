from django.utils import six
from events.backends.email import EmailBackend
from django.contrib.auth.models import User
from events.models import EventType
from django.contrib.sites.models import Site


def send_html_email(to, sender, label, **kwargs):
    '''
    template_name is the slug of the template to use for this message (see
        models.EmailTemplate)

    context is a dictionary to be used when rendering the template

    'to' can be either a string, eg 'a@b.com', or a list of strings.
    
    from_email should contain a string, eg 'My Site <me@z.com>'. If you leave it
        blank, it'll use settings.DEFAULT_FROM_EMAIL as a fallback.

    fail_silently is passed to Django's mail routine. Set to 'True' to ignore
        any errors at send time.

    files can be a list of file paths to be attached, or it can be left blank.
        eg ('/tmp/file1.txt', '/tmp/image.png')
    
    '''
        
    notice_type = EventType.objects.get(label=label)
    scoping = kwargs.get('scoping', None)
    if isinstance(to, six.string_types):
        users = User.objects.filter(groups__name=to)

    backend = EmailBackend()
    for user in users:   
        if backend.can_send(user,notice_type,scoping):
            backend.deliver(user, sender, notice_type, **kwargs)
