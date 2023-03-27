from django import forms
from django.contrib.admin import widgets

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder



class PreviewForm(forms.Form):

    object_list = forms.CharField(
        label = "List of objects",
        max_length = 500,
    )
    
    def __init__(self, *args, **kwargs):
        super(PreviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-previewForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''


        self.helper.add_input(Submit('submit', 'Submit'))