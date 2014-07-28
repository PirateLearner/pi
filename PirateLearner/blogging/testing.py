import .tag_lib
from django.db import models
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class Testing(models.Model):
	Author = CharField(Max_length=100)
	 tag_list = [  { 'name':'Author_tag' , 'type' :'CharField'} ,]

	def __init__(self):
		self.Author = " "
	def __str__(self):
		return "Testing"

	def render_to_template(self,db_object):
		for tag_name in self.tag_list:
			result_field = tag_lib.parse_content(db_object,tag_name)
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			if current_field == 'Author' : 
				tagged_field = tag_start + self.title + tag_end 
				self.Author = result_field 

	def render_to_db(self,db_object):
		for tag_name in self.tag_list:
			current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
			tag_start = "%% " + str(tag_name["name"]) + " %%" 
			tag_end = "%% endtag " + str(tag_name["name"]) + " %%"
			if current_field == 'Author' : 
				tagged_field = tag_start + self.Author + tag_end 
				db_object.content += tagged_field 

