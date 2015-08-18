from django import forms
from django.utils.translation import ugettext_lazy as _

from bookmarks.models import BookmarkInstance, BookmarkFolderInstance, PRIVACY, LatestBookmarksPlugin
from taggit.models import Tag
from django_select2.fields import AutoModelSelect2TagField,AutoModelSelect2MultipleField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from bookmarks.widgets import SelectWithPopUp
from django.core.urlresolvers import reverse
from bookmarks import utils
from bookmarks import settings
from ckeditor.widgets import CKEditorWidget

class TagField(AutoModelSelect2TagField):
    queryset = Tag.objects.all()
    search_fields = ['name__icontains', ]
    def get_model_field_values(self, value):
        return {'name': value}


      
class BookmarkFolderForm(forms.ModelForm):
    description = forms.Textarea()
    
    def __init__(self, user, *args, **kwargs):
        super(BookmarkFolderForm, self).__init__(*args, **kwargs)
        self.user = user
        # hack to order fields
        self.fields.keyOrder = ["title", "description"]
        #super(BookmarkInstanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.helper.form_id = 'id-BookmarkFolderForm'
#        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('bookmarks:add-model-folder',kwargs = {'model_name': 'folder'})
        self.helper.layout = Layout(
                Fieldset(
                'Create the Folder!!!',
                'title',
                'description',
            ),
            
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
            
            )
  
    def clean(self):
        if not self.cleaned_data.get("title", None):
            return self.cleaned_data
        if BookmarkFolderInstance.objects.filter(title=self.cleaned_data["title"], adder=self.user).count() > 0:
            raise forms.ValidationError(_("You already have this folder."))
        return self.cleaned_data
                
    class Meta:
        model = BookmarkFolderInstance
        fields = [
            "title",
            "description",
        ]

class BookmarkInstanceForm(forms.ModelForm):
    
    url = forms.URLField(label = "URL", required=True, widget=forms.TextInput(attrs={"size": 100}))
    description = forms.Textarea()
    note = forms.CharField(widget = CKEditorWidget(config_name='author'), required=False)
    tags = TagField()
    folder = forms.ModelChoiceField(queryset = BookmarkFolderInstance.objects.all(),
                    empty_label="-----",
                    required = True,
                    label = "Select Folder or Create New!",
                    widget=SelectWithPopUp)
#    redirect = forms.BooleanField(label="Redirect", required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(BookmarkInstanceForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['folder'].queryset = BookmarkFolderInstance.objects.filter(adder=user)
        # hack to order fields
        self.fields.keyOrder = ["url", "folder", "title", "description","note", "image_url","privacy_level","tags"]
        #super(BookmarkInstanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.helper.form_id = 'id-BookmarkInstanceForm'
#        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('bookmarks:add_bookmark')
        self.helper.layout = Layout(
                Fieldset(
                'Create the bookmark by entring the URL!!!',
                'url',
                'folder',
                'title',
                'description',
                'note',
                Field('image_url', type="hidden", required=False),
                'privacy_level',
                'tags',
            ),
            
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
            
            )
    
    def clean(self):
        if not self.cleaned_data.get("url", None):
            return self.cleaned_data
        self.cleaned_data["url"] = utils.strip_url(self.cleaned_data["url"])
            
        if BookmarkInstance.objects.filter(bookmark__url=self.cleaned_data["url"], user=self.user).count() > 0:
            raise forms.ValidationError(_("You have already bookmarked this link."))
        return self.cleaned_data
                
    def should_redirect(self):
        if self.cleaned_data["redirect"]:
            return True
        else:
            return False
    
    def save(self, commit=True):
#        self.instance.url = self.cleaned_data["url"]
        return super(BookmarkInstanceForm, self).save(commit)
    
    class Meta:
        model = BookmarkInstance
        fields = [
            "url",
            "folder",
            "title",
            "description",
            "note",
            "image_url",
            "privacy_level",
        ]
        
        

class BookmarkInstanceUpdateForm(forms.Form):
    title = forms.CharField(max_length = 100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    note = forms.CharField(widget = CKEditorWidget(config_name='author'), required=False)
    tags = TagField()
    folder = forms.ModelChoiceField(queryset = BookmarkFolderInstance.objects.all(),
                    empty_label="-----",
                    required = True,
                    label = "Select Folder or Create New!",
                    widget=SelectWithPopUp)
    
    privacy_level = forms.ChoiceField(choices=PRIVACY, required=True) 
    
    def __init__(self,user,bookmark_id, *args, **kwargs):
        super(BookmarkInstanceUpdateForm, self).__init__(*args, **kwargs)
        # hack to order fields
        self.fields['folder'].queryset = BookmarkFolderInstance.objects.filter(adder=user)
        self.bookmark_id = bookmark_id
        self.fields.keyOrder = ["title","folder", "description","note", "privacy_level","tags"]
        #super(BookmarkInstanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.helper.form_id = 'id-BookmarkInstanceUpdateForm'
#        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('bookmarks:update_bookmark_instance',args = bookmark_id)
        self.helper.layout = Layout(
                Fieldset(
                'EDIT BOOKMARK!!!',
                'folder',
                'title',
                'description',
                'note',
                'privacy_level',
                'tags',
            ),
            
            ButtonHolder(
                Submit('submit', 'Update', css_class='button white'),
                Submit('submit', 'Delete', css_class='button white')
            ),

            )
    
    def save(self, commit=True):
        instance = BookmarkInstance.objects.get(pk=self.bookmark_id)
        instance.title = self.cleaned_data["title"]
        instance.description = self.cleaned_data["description"]
        instance.note = self.cleaned_data["note"]
        instance.folder = self.cleaned_data["folder"]
        instance.privacy_level = self.cleaned_data["privacy_level"]
        return instance

class TagSelectField(AutoModelSelect2MultipleField):
    queryset = Tag.objects.all()
    search_fields = ['name__icontains', ]
    def get_model_field_values(self, value):
        return {'name': value}

    
class LatestBookmarksForm(forms.ModelForm):
    tags = TagSelectField()
    class Meta:
        model = LatestBookmarksPlugin