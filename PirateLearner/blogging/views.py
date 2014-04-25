from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib import auth
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from models import *
from django.http import HttpResponse


#from utils import *
import os
# Create your views here.

"""
def add_content_type(request):
    class_members = {}
    if request.method == 'POST':
        #Read the POST variable for class name
        name = request.POST.get('class_name','')
        #validate if this class already exists
        #until I know how to do that, and because I've decided to et each class get its own file
        #lets just try to open that file and if it fails, we are good to go :P
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
            for i in range (1, int(request.POST.get('num_val',''))+1):
                class_members[request.POST.get('val_%d' %i)] = request.POST.get('valtype_%d' %i)
                print class_members[request.POST.get('val_%d' %i)]
            create_class_object = CreateClass(name, class_members)
            string = create_class_object.form_string()
            try:
                fd = os.fdopen(os.open(filename,os.O_CREAT| os.O_RDWR , 0555),'w')
                fd.write(string)
                fd.close()
                print file(filename).read()
                errorstring +="\n"+file(filename).read()
	    except IOError:
                print "Error Opening File for Writing"
                errorstring += "\nError Opening file for writing"
        else:
            errorstring+="\nFile already exists"
            response = "<html><body>"+errorstring+"</body></html>"
    template = loader.get_template('elements/admin/type_form.html')
    context = RequestContext(request, {
                                       'string': "i am not here",
                                      })
    return HttpResponse(template.render(context))
"""
def index(request):
#    output = 'Welcome to the section page !!!'
#    print "IP Address for debug-toolbar: " + request.META['REMOTE_ADDR']
#    output += " ".join(path)
#    print path
    template = loader.get_template('blogging/section.html')
    context = RequestContext(request, {
                                       'nodes': BlogParent.objects.all().filter(level=0),
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
    return HttpResponse(template.render(context))


def authors_list(request):
	return HttpResponse("Hi This is author list view ")

def author_post(request,slug,post_id):
	return HttpResponse("Hi This is author post view")

def archive(request):	
	return HttpResponse("Hi This is archive view")

def teaser(request,slug):
	current_section = slug.split("/")[-1]
#	print current_section
	try:
		post_id = int(current_section)
		print "This is Detail page "
		
		template = loader.get_template('blogging/detail.html')
                context = RequestContext(request, {
                                       'nodes': BlogContent.objects.get(pk=post_id),
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
		return HttpResponse(template.render(context))
	except ValueError:
		try:
			section = BlogParent.objects.get(slug = str(current_section))
		except :	
			return HttpResponse("Hi SomeThing Got Wrong!!! ")
		if section.is_leaf_node():
			template = loader.get_template('blogging/teaser.html')
		        context = RequestContext(request, {
                                       'nodes': BlogContent.objects.all().filter(section=section),
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
                	return HttpResponse(template.render(context))
		template = loader.get_template('blogging/section.html')
		context = RequestContext(request, {
                                       'nodes': section.get_descendants(),
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
		return HttpResponse(template.render(context))
	
