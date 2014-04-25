from django.db import models
import tag_lib
class BaseContent(models.Model):
    title = models.CharField(max_length = 200)
    title_field_type = ""
    content = models.TextField()
    content_field_type = ""
    title_tag = {'name': "title_tag",'type':"Text"}
    content_tag = {'name': "content_tag",'type':"Text"}
    tag_list = [title_tag,content_tag]
    def __init__(self):
        self.title = ""
        self.content = ""
    def __str__(self):
        return "BaseContent"
    

    def render_to_template(self,db_object):
        for tag_name in self.tag_list:
            result_field = tag_lib.parse_content(db_object,tag_name)
            current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
            if current_field == 'title':
                self.title = result_field
            if current_field == 'content':
                self.content = result_field
                
    def render_to_db(self,db_object):
        
        for tag_name in self.tag_list:
            current_field = tag_lib.get_field_name_from_tag(str(tag_name['name']))
            tag_start = "%% " + str(tag_name["name"]) + " %%" 
            tag_end = "%% endtag " + str(tag_name["name"]) + " %%"
            if current_field == 'title':
                tagged_field = tag_start + self.title + tag_end
                db_object.title = tagged_field 
            if current_field == 'content':
                tagged_field = tag_start + self.content + tag_end
                db_object.content += tagged_field 
             

