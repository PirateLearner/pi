from django import forms
from django.contrib.admin import widgets
from dashboard.models import *
from taggit.models import Tag
# from django_select2 import *
# from django_select2.widgets import Select2MultipleWidget


# class TagField(AutoModelSelect2MultipleField):
#     queryset = Tag.objects.all()
#     search_fields = ['name__icontains', ]
#     def get_model_field_values(self, value):
#         return {'name': value}

class ProfileEditForm(forms.ModelForm):

    #interest = forms.MultipleChoiceField(widget = Select2MultipleWidget(choices = Tag.objects.all()))
    print("LOGS: ProfileEditForm()--> interest are : ", Tag.objects.all())
    address = forms.Textarea()
    occupation = forms.ChoiceField(choices=OCCUPATION)
    website = forms.CharField()
    date_of_birth = forms.DateField()
#     interest = TagField()
    class Meta:
        model = UserProfile
        exclude = (
                   'gender',
                   'user'
                   )

