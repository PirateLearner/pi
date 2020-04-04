from django import forms
from django.utils.translation import ugettext_lazy as _

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
# from django_select2.fields import AutoModelSelect2MultipleField
from taggit.models import Tag
# from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from django.urls import reverse
from spotlight.models import  TYPE
# import django_select2
class SpotlightForm(forms.Form):

    url = forms.URLField(label = "URL", required=True, widget=forms.TextInput(attrs={"size": 100}))
    type = forms.ChoiceField(choices=TYPE)

    def __init__(self, *args, **kwargs):
        super(SpotlightForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ["url", "type"]
#         self.helper = FormHelper()
#
#         self.helper.form_id = 'id-SpotlightForm'
# #        self.helper.form_class = 'blueForms'
#         self.helper.form_class = 'form-horizontal'
#         self.helper.label_class = 'col-lg-2'
#         self.helper.field_class = 'col-lg-8'
#         self.helper.form_method = 'post'
#         self.helper.form_action = reverse('spotlight:add_spotlight')
#         self.helper.layout = Layout(
#                 Fieldset(
#                 'Create the Spotlight!!!',
#                 'url',
#                 'type',
#             ),
#
#             ButtonHolder(
#                 Submit('submit', 'Submit', css_class='button white')
#             ),
#
#             )
#
# class TagSelectField(AutoModelSelect2MultipleField):
#     queryset = Tag.objects.all()
#     search_fields = ['name__icontains', ]
#     def get_model_field_values(self, value):
#         return {'name': value}
#
#
# class LatestSpotlightForm(forms.ModelForm):
#
#     class Meta:
#         model = LatestSpotlightPlugin
#         widgets = {
#             'tags': django_select2.Select2MultipleWidget
#         }
