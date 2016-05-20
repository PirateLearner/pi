import os
from blogging.create_class import CreateClass, CreateTemplate
import re
from django.utils.functional import allow_lazy
from django.utils import six
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import user_passes_test
import unicodedata

def create_content_type(name,form_dict,is_leaf):
	"""
	This function will create the form and template for new contentype
	"""
	form_filename = os.path.abspath(os.path.dirname(__file__))+"/custom/"+name.lower()+".py"
	template_filename = os.path.abspath(os.path.dirname(__file__))+"/templates/blogging/includes/"+name.lower()+".html"
	flag = False
	try:
		fd = open(form_filename, 'r')
		fd.close()
		fd1 = open(template_filename, 'r')
		fd1.close()
	except IOError:
		flag = True
	if flag:
		#We are good to go. Create the Output string that must be put in it
		create_class_object = CreateClass(name, form_dict,is_leaf)
		form_string = create_class_object.form_string()
		template_object = CreateTemplate(name, form_dict,is_leaf)
		template_string = template_object.form_string() 
		
		try:
			fd = os.fdopen(os.open(form_filename,os.O_CREAT| os.O_RDWR , 0555),'w')
			fd.write(form_string)
			fd.close()
			fd = os.fdopen(os.open(template_filename,os.O_CREAT| os.O_RDWR , 0555),'w')
			fd.write(template_string)
			fd.close()
			
			print file(form_filename).read()
			return True
		except IOError:
			print "Error Opening File for Writing"
			return False
	else:
		return False

	
	
	

def get_imageurl_from_data(data):
	
	try:
		matches = re.findall(
				r'(<img[^>].*?src\s*=\s*"([^"]+)")', data
			)
		if matches:
			return str(matches[0][1])
		else:
			return None
	except:
		print "Error in get_imageurl_from_data"
		return None


def strip_image_from_data(data):	
	p = re.compile(r'<img.*?/>',flags=re.DOTALL)
	line = p.sub('', data)
	print "LOGS:: Stripping images from data"
	return line
	
def truncatewords(Value,limit=30):
	try:
		limit = int(limit)
		# invalid literal for int()
	except ValueError:
		# Fail silently.
		return Value

	# Make sure it's unicode
	Value = unicode(Value)

	# Return the string itself if length is smaller or equal to the limit
	if len(Value) <= limit:
		return Value

	# Cut the string
	Value = Value[:limit]

	# Break into words and remove the last
	words = Value.split(' ')[:-1]

	# Join the words and return
	return ' '.join(words) + '...'

def slugify_name(value):
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub('[^\w\s-]', '', value).strip().lower()
	return mark_safe(re.sub('[-\s]+', '_', value))



def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

slugify_name = allow_lazy(slugify_name, six.text_type)
