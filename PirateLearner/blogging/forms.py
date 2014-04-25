from django import forms
from djangocms_text_ckeditor.fields import HTMLField

from blogging.models import BlogContent
import django_select2
import taggit

"""
class LatestEntriesForm(forms.ModelForm):

    class Meta:

        widgets = {
            'tags': django_select2.Select2MultipleWidget
        }
"""

class PostTagWidget(django_select2.widgets.Select2Mixin, taggit.forms.TagWidget):

    def __init__(self, *args, **kwargs):
        options = kwargs.get('select2_options', {})
        options['tags'] = list(taggit.models.Tag.objects.values_list('name', flat=True))
        options['tokenSeparators'] = [',',]
        kwargs['select2_options'] = options
        super(PostTagWidget, self).__init__(*args, **kwargs)

    def render_js_code(self, *args, **kwargs):
        js_code = super(PostTagWidget, self).render_js_code(*args, **kwargs)
        return js_code.replace('$', 'jQuery')


class PostForm(forms.ModelForm):

    class Meta:
        widgets = {'tags': PostTagWidget}





class PostEditForm(forms.ModelForm):
    data = HTMLField()

    class Meta:
        model = BlogContent
        widgets = {'tags': PostTagWidget}
        exclude = (
            'page',
            'create_date',
            'author_id',
            'special_flag',
            'published_flag',
	    'last_modefied',
	    'url_path',
	    'objects',
        )

class LatestEntriesForm(forms.ModelForm):

    class Meta:

        widgets = {
            'tags': django_select2.Select2MultipleWidget
        }


