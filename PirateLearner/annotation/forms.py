from django import forms

from django.utils.translation import ungettext, ugettext, ugettext_lazy as _
from django.utils.text import get_text_list
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.conf import settings

from django_comments.forms import CommentSecurityForm
from annotation.models import Annotation


class AnnotationForm(CommentSecurityForm):
    body = forms.CharField(label=_('Annotate here'))
    privacy = forms.IntegerField()
    paragraph_id = forms.IntegerField()
    
    honeypot      = forms.CharField(required=False,
                                    label=_('If you enter anything in this field '\
                                            'your comment will be treated as spam'))

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value
    
    def get_comment_model(self):
        """
        Get the comment model to create with this form. Subclasses in custom
        comment apps should override this, get_comment_create_data, and perhaps
        check_for_duplicate_comment to provide custom comment models.
        """
        # Use our custom comment model instead of the default one.
        return Annotation

    def get_comment_create_data(self, request):
        """
        Returns the dict of data to be used to create a comment. Subclasses in
        custom comment apps that override get_comment_model can override this
        method to add extra fields onto a custom comment model.
        """
        data = {}
        #Do some additional work
        data['body'] = self.cleaned_data['body']
        data['privacy'] = self.cleaned_data['privacy']
        data['user_id'] = request.user.id #Check
        data['content_type'] = ContentType.objects.get_for_model(self.target_object)
        data['object_pk']    = force_text(self.target_object._get_pk_val())
        data['site_id']      = settings.SITE_ID
        data['paragraph_id'] = 0
        if 'paragraph_id' in self.cleaned_data:
            data['paragraph_id'] = self.cleaned_data['paragraph_id']
                
        return data
    
    def get_comment_object(self, request):
            """
            Return a new (unsaved) comment object based on the information in this
            form. Assumes that the form is already validated and will throw a
            ValueError if not.
    
            Does not set any of the fields that would come from a Request object
            (i.e. ``user`` or ``ip_address``).
            """
            if not self.is_valid():
                raise ValueError("get_comment_object may only be called on valid forms")
    
            CommentModel = self.get_comment_model()
            new = CommentModel(**self.get_comment_create_data(request))
            new = self.check_for_duplicate_comment(new)
    
            return new
    

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = self.get_comment_model()._default_manager.using(
            self.target_object._state.db
        ).filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
            user_id = new.user_id, #Check
        )
        for old in possible_duplicates:
            if old.body == new.body:
                return old

        return new

    def clean_comment(self):
        """
        If COMMENTS_ALLOW_PROFANITIES is False, check that the comment doesn't
        contain anything in PROFANITIES_LIST.
        """
        comment = self.cleaned_data["body"]
        if settings.COMMENTS_ALLOW_PROFANITIES == False:
            bad_words = [w for w in settings.PROFANITIES_LIST if w in comment.lower()]
            if bad_words:
                raise forms.ValidationError(ungettext(
                    "Watch your mouth! The word %s is not allowed here.",
                    "Watch your mouth! The words %s are not allowed here.",
                    len(bad_words)) % get_text_list(
                        ['"%s%s%s"' % (i[0], '-'*(len(i)-2), i[-1])
                         for i in bad_words], ugettext('and')))
        return comment

    

    
    