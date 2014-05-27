from django import forms
from djangocms_text_ckeditor.fields import HTMLField
from django.contrib.admin import widgets
from blogging.models import *
import django_select2
import taggit
from djangocms_text_ckeditor.widgets import TextEditorWidget
from blogging.widgets import SelectWithPopUp
from django.db import models
from ckeditor.widgets import CKEditorWidget

CUSTOM_FIELD_TYPE  = (
	('CharField', 'Text'),
	('ImageField', 'Image'),
	('FileField','File Upload'),
)

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

	data = forms.CharField(label="Data Field", widget=CKEditorWidget())
	class Meta:
		widgets = {'tags': PostTagWidget,}
		model= BlogContent

class ParentForm(forms.ModelForm):

	data = forms.CharField(label="Data Field", widget=CKEditorWidget(),help_text=('Please Upload at least one picture for preview!!!'))
	class Meta:
		model= BlogParent


class ContentTypeForm(forms.Form):
	ContentType = forms.ModelChoiceField(queryset = BlogContentType.objects.all(),empty_label=None,widget = SelectWithPopUp)


class ContentTypeCreationForm(forms.ModelForm):
	class Meta:
		model = BlogContentType

class FieldTypeForm(forms.Form):
	field_name = forms.CharField('Field Name')
	field_type = forms.MultipleChoiceField(choices =CUSTOM_FIELD_TYPE)
	
class ContentForm(forms.ModelForm):
	class Meta:
		model = BlogContent

class PostEditForm(forms.ModelForm):

    class Meta:
        model = BlogContent
        widgets = {'tags': PostTagWidget,
		   'publication_start': widgets.AdminSplitDateTime }
        exclude = (
            'page',
            'create_date',
            'author_id',
            'special_flag',
            'published_flag',
	    'last_modefied',
	    'url_path',
	    'objects',
	    'slug',
        )

class LatestEntriesForm(forms.ModelForm):

    class Meta:

        widgets = {
            'tags': django_select2.Select2MultipleWidget
        }
class SectionPluginForm(forms.ModelForm):
	
	class Meta:
		model = SectionPlugin
	
	def __init__(self, *args, **kwargs):
		super(SectionPluginForm, self).__init__(*args, **kwargs)
		choices = [self.fields['parent_section'].choices.__iter__().next()]
		for page in self.fields['parent_section'].queryset:
			choices.append(
				(page.id, ''.join(['-'*page.level, page.__unicode__()]))
			)
		self.fields['parent_section'].choices = choices



"""
class PageForm(forms.Form):
        title = forms.CharField()
	parent = forms.ModelChoiceField(queryset= BlogParent.objects.filter(children=None) , empty_label=None)
	content_type = forms.ModelChoiceField(queryset = BlogContentType.objects.all(),empty_label=None)
        body = forms.CharField( widget=TextEditorWidget(attrs = {'toolbar': 'HTMLField'}) )

        def clean_title(self):
                title = self.cleaned_data['title']
                num_words = len(title.split())
                if num_words < 4:
                    raise forms.ValidationError("Not enough words!")
                return title

        def clean_body(self):
                body = self.cleaned_data['body']
                num_words = len(body.split())
                if num_words < 4:
                    raise forms.ValidationError("Not enough words!")
                return body


"""
