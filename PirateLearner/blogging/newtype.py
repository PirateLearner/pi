import tag_lib
from django.db import models
from blogging.models import *
from django import forms
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class Newtype(models.Model):
	content_list = models.CharField()
	title = models.CharField()
	tag_list = [  { 'name':'content_list_tag' , 'type' :'CharField'} , { 'name':'title_tag' , 'type' :'CharField'} ,]

	def __init__(self,content_list,title):
		self.content_list = content_list
		self.title = title
	def __str__(self):
		return "NewType"

	def render_to_template(self,db_object):
		for tag_name in self.tag_list:
			result_field = tag_lib.parse_content(db_object,tag_name)
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			if current_field == 'content_list' : 
				tagged_field = tag_start + self.title + tag_end 
				self.content_list = result_field 

			if current_field == 'title' : 
				tagged_field = tag_start + self.title + tag_end 
				self.title = result_field 

	def render_to_db(self,db_object):
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			tag_start = "%% " + str(tag_name["name"]) + " %%" 
			tag_end = "%% endtag " + str(tag_name["name"]) + " %%"
			if current_field == 'content_list' : 
				tagged_field = tag_start + self.content_list + tag_end 
				db_object.data += tagged_field 

			if current_field == 'title' : 
				tagged_field = tag_start + self.title + tag_end 
				db_object.title += tagged_field 

class NewTypeForm(forms.ModelForm):
	title = forms.CharField()
	class Meta:
		model = BlogParent
		fields = ("title","preview_image","parent")
