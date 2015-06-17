from blogging import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import TagField
from ckeditor.widgets import CKEditorWidget
from django.db.models import Q 
from mptt.forms import TreeNodeChoiceField 
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class Chapter(models.Model):
	title = models.CharField(max_length=100)
	Summary = models.TextField()
	tag_list = [  { 'name':'title_tag' , 'type' :'CharField'} , { 'name':'Summary_tag' , 'type' :'TextField'} ,]

	def __str__(self):
		return "Chapter"

	def render_to_template(self,db_object):
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			result_field = tag_lib.parse_content(db_object,tag_name)
			if current_field == 'title' : 
				self.title = result_field 

			if current_field == 'Summary' : 
				self.Summary = result_field 

	def render_to_db(self,db_object):
		temp_data = ""
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			tag_start = "%% " + str(tag_name["name"]) + " %% " 
			tag_end = "%% endtag " + str(tag_name["name"]) + " %%"
			if current_field == 'title' : 
				tagged_field = tag_start + self.title + tag_end 
				db_object.title = self.title 

			if current_field == 'Summary' : 
				tagged_field = tag_start + self.Summary + tag_end 
				temp_data += tagged_field 

		db_object.data = temp_data

class ChapterForm(forms.ModelForm):
	Summary =  forms.CharField(widget = CKEditorWidget())
	parent = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),~Q(title="Blog")),required=True,empty_label=None, label = "Select Parent" )
	class Meta:
		model = Chapter
	def save(self):
		instance = Chapter()
		instance.title = self.cleaned_data["title"]
		instance.Summary = self.cleaned_data["Summary"]
		return instance
