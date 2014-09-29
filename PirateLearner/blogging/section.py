import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import *
from ckeditor.widgets import CKEditorWidget
from taggit.forms import * 
from django.db.models import Q 
from mptt.forms import TreeNodeChoiceField 
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class Section(models.Model):
	title = models.CharField(max_length=100)
	Preface = models.TextField()
	Summary = models.TextField()
	tag_list = [ { 'name':'title_tag' , 'type' :'CharField'},  { 'name':'title_tag' , 'type' :'CharField'} , { 'name':'Preface_tag' , 'type' :'TextField'} , { 'name':'Summary_tag' , 'type' :'TextField'} ,]

	def __init__(self):
		self.title = " "
		self.Preface = " "
		self.Summary = " "
	def __str__(self):
		return "Section"

	def render_to_template(self,db_object):
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			result_field = tag_lib.parse_content(db_object,tag_name)
			if current_field == 'title' : 
				self.title = result_field 

			if current_field == 'Preface' : 
				self.Preface = result_field 

			if current_field == 'Summary' : 
				self.Summary = result_field 

	def render_to_db(self,db_object):
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			tag_start = "%% " + str(tag_name["name"]) + " %%" 
			tag_end = "%% endtag " + str(tag_name["name"]) + " %%\n"
			if current_field == 'title' : 
				db_object.title = self.title 

			if current_field == 'Preface' : 
				tagged_field = tag_start + self.Preface + tag_end 
				db_object.data += tagged_field 

			if current_field == 'Summary' : 
				tagged_field = tag_start + self.Summary + tag_end 
				db_object.data += tagged_field 

class SectionForm(forms.ModelForm):
	Preface =  forms.CharField(widget = CKEditorWidget())
	Summary =  forms.CharField(widget = CKEditorWidget())
	parent = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),~Q(title="Blog")),required=True, label = "Select Parent" )
	class Meta:
		model = Section
	def save(self):
		instance = Section()
		instance.title = self.cleaned_data["title"]
		instance.Preface = self.cleaned_data["Preface"]
		instance.Summary = self.cleaned_data["Summary"]
		return instance

		
