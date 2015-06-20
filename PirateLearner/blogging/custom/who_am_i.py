from blogging import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import *
from ckeditor.widgets import CKEditorWidget
import json
from django.db.models import Q 
from mptt.forms import TreeNodeChoiceField
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class Who_am_iForm(forms.Form):
	title = forms.CharField(max_length = 100)
	pid_count = forms.IntegerField(required=False)
	section = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),Q(children=None)),required=True,empty_label=None, label = "Select Section" )
	i_dont_know = forms.CharField(max_length=100, required=False)
	why_not = forms.CharField(widget = CKEditorWidget(), required=False)
	tags = TagField()
	def __init__(self,action, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = "id-TestFormClass"
		self.helper.form_class = "form-horizontal"
		self.helper.label_class = "col-lg-2"
		self.helper.field_class = "col-lg-8"
		self.helper.form_method = "post"
		self.helper.form_action = action
		self.helper.layout = Layout(
			Fieldset(
			"Create The Content of Type Who_am_i ",
			"title",
			"i_dont_know",
			"why_not",
			"section",
			Field("pid_count", type="hidden"),

			"tags",
			 ),
			ButtonHolder(
			Submit("submit", "Submit", css_class="button white")
			),
		)
		super(Who_am_iForm, self).__init__(*args, **kwargs)



	def save(self,post):
		post.pop("csrfmiddlewaretoken")
		post.pop("submit")
		post.pop("title")
		post.pop("section")
		for k,v in post.iteritems():
			if str(k) != "pid_count" :
				tmp = {}
				tmp = tag_lib.insert_tag_id(str(v), post["pid_count"])
				post[k] = tmp["content"]
				post["pid_count"] = tmp["pid_count"]
		return json.dumps(post.dict())
