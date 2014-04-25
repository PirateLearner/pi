from models import *
import content_type
import re
import os

def project_path():
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    print PROJECT_PATH

def get_pattern(current_tag):
    tag_start_pattern = "\\%\\% " + str(current_tag['name']) + " \\%\\%"
    tag_end_pattern = "\\%\\% endtag "+ str(current_tag['name']) + " \\%\\%"
    final_pattern = tag_start_pattern + "(.*?)" + tag_end_pattern
    return final_pattern

def get_field_name_from_tag(current_tag):
    field_name = current_tag.split("_")[0:-1]
    return_name = "_".join(str(tag) for tag in field_name)
    return return_name
    
def parse_content(data, tag):
    final_pattern = get_pattern(tag)
    patt = re.compile(final_pattern)
    result = patt.search(data)
    return result.group(1)

def insert_tag_into_content(data,tag):
    tag_start = "\%\% " + str(tag["name"]) + " \%\%" 
    tag_end = "\%\% endtag " + str(tag["name"]) + " \%\%" 
    print type(data)
    print data
    return_field = tag_start + str(data) + tag_end
    print "rebuilding tags " + return_field
    return return_field
 
def render_to_template(db_class_name,content_type_name):
    render_class = getattr(content_type,content_type_name)
    render_object = render_class()
    render_object.title = "Hi, I am converted"
    data  = """
    This is data %% title_tag %% this is inside title tag %% endtag title_tag %% 
    Something eles.
    %% content_tag %% This is inside content tage %% endtag content_tag %%
    """
    print data
    #print type(render_object)
    #print render_object.title
    if db_class_name == 'Content':
        render_object.title = db_class_name.title
        for tag_name in render_object.tag_list:
            result_field = parse_content(data,tag_name)
            current_field = get_field_name_from_tag(str(tag_name['name']))
            render_object_field = getattr(render_object,str(current_field))
            render_object_field = result_field
            print render_object_field
    
    render_to_db(render_object,"something")
    return render_object

def render_to_db(wrapper_object,db_object):
    
    print "rendering to db object"
    if wrapper_object:
        for tag_name in wrapper_object.tag_list:
            current_field = get_field_name_from_tag(str(tag_name['name']))
            render_object_field = getattr(wrapper_object,str(current_field))
            print render_object_field
            tag_start = "\%\% " + str(tag_name["name"]) + " \%\%" 
            tag_end = "\%\% endtag " + str(tag_name["name"]) + " \%\%" 
            print tag_start + render_object_field + tag_end 
            #feed_content = insert_tag_into_content(render_object_field,tag_name)
            if str(current_field) == 'title':
                #db_object.title = feed_content
                print "It is title"
            else:
                #db_object.content += feed_content
                print "it is content"
         
def find_class(content_type):
    render_module = getattr(elements,content_type)
    print type(render_module)
    render_class = getattr(render_module,content_type)
    print type(render_class)
    
