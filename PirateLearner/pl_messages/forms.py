__author__ = 'aquasan'

from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Messages


class MessageForm(forms.Form):
    to = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    body = forms.CharField(label='Message', widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    
    def __init__(self,user,*args,**kwargs):
        super(MessageForm,self ).__init__(*args,**kwargs)
        self.fields['to'].queryset = User.objects.exclude(id=user.id)        

class ReplyForm(forms.Form):
    body = forms.CharField(widget= forms.Textarea(attrs={'cols': 80, 'rows': 5}))