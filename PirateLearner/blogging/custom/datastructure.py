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
class DatastructureForm(forms.Form):
	title = forms.CharField(max_length = 100)
	pid_count = forms.IntegerField(required=False)
	section = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),Q(children=None)),required=True,empty_label=None, label = "Select Section" )
	tags = TagField(help_text= "comma seperated fields for tags")
	Note = forms.CharField(widget = CKEditorWidget(), required=False)
	Description = forms.CharField(widget = CKEditorWidget(), required=False)
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = "id-TestFormClass"
		self.helper.form_class = "form-horizontal"
		self.helper.label_class = "col-lg-2"
		self.helper.field_class = "col-lg-8"
		self.helper.form_method = "post"
		self.helper.form_action = reverse("blogging:create-post")
		self.helper.layout = Layout(
			Fieldset(
			"Create The Content of Type Datastructure ",
			"title",
			"section",
			Field("pid_count", type="hidden"),
			"Note",
			"Description",
			"tags",
			 ),
			ButtonHolder(
			Submit("submit", "Submit", css_class="button white")
			),
		)
		super(DatastructureForm, self).__init__(*args, **kwargs)



	def save(self,post,db_instance=None):
		post.pop("csrfmiddlewaretoken")
		post.pop("submit")
		post.pop("title")
		if db_instance != None:
			instance = db_instance
		else:
			instance = BlogContent()
		instance.title = self.cleaned_data["title"]
		instance.section = self.cleaned_data["section"]
		pid_count = self.cleaned_data["pid_count"]
		post.pop("section")
		for k,v in post.iteritems():
			if str(k) != "pid_count" :
				tmp = {}
				tmp = tag_lib.insert_tag_id(str(v),pid_count )
				post[k] = tmp["content"]
				post["pid_count"] = tmp["pid_count"]
		json_str = json.dumps(post.dict())
		instance.data = str(json_str)
		return instance


