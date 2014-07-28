import tag_lib
from django.db import models
from blogging.models import *
from django import forms
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class Hi(models.Model):
	model_name = models.CharField(max_length=100)
	title = models.CharField()
	tag_list = [  { 'name':'title_tag' , 'type' :'CharField'} ,]

	def __init__(self):
		self.title = " "
	def __str__(self):
		return "Hi"

	def render_to_template(self,db_object):
		for tag_name in self.tag_list:
			result_field = tag_lib.parse_content(db_object,tag_name)
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			if current_field == 'title' : 
				tagged_field = tag_start + self.title + tag_end 
				self.title = result_field 

	def render_to_db(self,db_object):
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			tag_start = "%% " + str(tag_name["name"]) + " %%" 
			tag_end = "%% endtag " + str(tag_name["name"]) + " %%"
			if current_field == 'title' : 
				tagged_field = tag_start + self.title + tag_end 
				db_object.title += tagged_field 

class HiForm(forms.ModelForm):
	title = forms.CharField()
	class Meta:
		model = BlogContent
		fields = ("title","section","tags")
		widgets = {"tags": PostTagWidget}
