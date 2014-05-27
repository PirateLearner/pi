from models import *
import os
from .create_class import CreateClass
from cms.plugin_pool import plugin_pool
import re

def create_content_type(name,formset,is_leaf):
	class_members = {}
	filename = os.path.abspath(os.path.dirname(__file__))+"/"+name.lower()+".py"
        flag = False
        errorstring = filename
        try:
            fd = open(filename, 'r')
        except IOError:
            flag = True
            print "No such file exists"
            errorstring += "\nNo such file exists"
        if flag:
            #We are good to go. Create the Output string that must be put in it
            print "We're in!"
            errorstring += "\nWe're in!"
	    for form in formset.forms:
		class_members[form.cleaned_data['field_name']] = form.cleaned_data['field_type'][0]
                print class_members[form.cleaned_data['field_name']]
            create_class_object = CreateClass(name, class_members,is_leaf)
            string = create_class_object.form_string()
            try:
                fd = os.fdopen(os.open(filename,os.O_CREAT| os.O_RDWR , 0555),'w')
                fd.write(string)
                fd.close()
                print file(filename).read()
                errorstring +="\n"+file(filename).read()
		return True
            except IOError:
                print "Error Opening File for Writing"
                errorstring += "\nError Opening file for writing"
		return False
	else:
	    return False
	   

def get_imageurl_from_data(data):
	matches = re.findall(
				r'(<img[^>]*?src\s*=\s*"([^"]+)")', data
			)
	if matches:
		print str(matches[0][1])
		return str(matches[0][1])
	else:
		return None



def strip_image_from_data(data):
	pat = r'(<img[^>]*?>)'
	m = re.search(pat,data)
	line= data
	if m and m.groups() > 0:
		line = data[:m.start(1)] + ' ' + data[m.end(1):]
		print line
	else:
		print "the pattern didn't capture any text"
	return line	
	

 
