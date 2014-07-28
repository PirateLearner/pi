"""@package PirateDocs 
	This is main view module for Blogging app supporting various view provided to the User.
"""


from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib import auth
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .create_class import CreateClass
from django.contrib.formtools.wizard.views import SessionWizardView
from django.forms.formsets import formset_factory
from django.utils.html import escape
from .utils import *
from wrapper import *
import os, errno
from django.db.models import Q
from django.core.mail import send_mail, mail_admins
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import reversion
from reversion.helpers import generate_diffs


# Create your views here.


@login_required
def content_type(request):
	"""
	This view ask user to choose content type from the existing one or 
	create new content type to fit for his/her needs to create post.
	Operations: 
	NEXT -- Go to next page for creation of New content based on selected content type.
	DELETE -- Delete the current selected content type (requires admin authorizations )
	NEW -- Create New content type.
	"""
	if request.method == "POST":
	    form = ContentTypeForm(request.POST)
	    if form.is_valid():
	    	action = request.POST.get('submit')
	    	content_info = form.cleaned_data['ContentType']
	    	
	    	if action == 'next':
		        
		        print content_info, type(content_info)
		        request.session['content_info_id'] = content_info.id
		        return HttpResponseRedirect(
		            reverse("blogging:create-post"))
	        if action == 'delete':
	        	try:
	        		filename = os.path.abspath(os.path.dirname(__file__))+"/"+content_info.__str__().lower()+".py"
	        		os.remove(filename)
        		except OSError as e: # this would be "except OSError, e:" before Python 2.6
			        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
			            raise # re-raise exception if a different error occured
   	        	content_info.delete()

	else:
	    if 'content_info_id' in request.session:
	        try:
	            content_info_obj = BlogContentType.objects.get(
	                id=request.session['content_info_id']
	            )
	            form = ContentTypeForm()
	        except ObjectDoesNotExist:
	            del request.session['content_info_id']
	            form = ContentTypeForm()
	    else:
	        form = ContentTypeForm()
	return render_to_response(
	    "blogging/content_type.html",
	    locals(), context_instance=RequestContext(request))	

@login_required
def new_post(request):
	"""
	Used for creating new post depending upon the content type chosen by the user in previous step.
	If content type is not selected then redirect to content-type page for selection of appropriate content type.
	Operations:
	BACK -- Go back to previous step for selecting new content type.
	SAVE -- Save the content as draft for later revision.
	SUBMIT -- Submit the post for moderation and publication. 
	"""
	if 'content_info_id' not in request.session:
		return HttpResponseRedirect(reverse("blogging:content-type"))
    
	content_info_obj = BlogContentType.objects.get(
	        id=request.session['content_info_id']
    )
	print request.session['content_info_id'], content_info_obj
	form = find_class('blogging.'+content_info_obj.__str__().lower(),str(content_info_obj)+'Form' )
	if request.method == "POST":
		post_form = form(request.POST)
		
		if post_form.is_valid():
			wrapper_class = post_form.save()
			db_class = None
			
			if content_info_obj.is_leaf == True:
				db_class = BlogContent()
				wrapper_class.render_to_db(db_class)
				db_class.section = post_form.cleaned_data['section']
				m_tags = post_form.cleaned_data['tags']
				db_class.content_type = content_info_obj
				db_class.slug = slugify(db_class.title)
				db_class.author_id =  request.user
				db_class.save()
				db_class.tags.add(*m_tags)
				
			else:
				db_class = BlogParent()
				wrapper_class.render_to_db(db_class)
				db_class.parent = post_form.cleaned_data['parent']
				db_class.slug = slugify(db_class.title)
				db_class.save()
			del request.session['content_info_id']
			context = {'success':True}
			return render_to_response(
									"blogging/create_page.html",
	    				context, context_instance=RequestContext(request))

		    ## Send them to a thank you page
	else:
		post_form = form()
	context = {'form':post_form}
	return render_to_response(
	    "blogging/create_page.html",
	    context, context_instance=RequestContext(request))



@login_required
def add_new_model(request, model_name):
	if (model_name.lower() == model_name):
		normal_model_name = model_name.capitalize()
	else:
		normal_model_name = model_name
	print normal_model_name
	
	if normal_model_name == 'ContentType' :
		FieldFormSet = formset_factory(FieldTypeForm,extra=4,max_num=1)
		helper = FormsetHelper()
		if request.method == 'POST':
			form1 = ContentTypeCreationForm(request.POST)
			form2 = FieldFormSet(request.POST)
	#			print form1.as_table()
	#			for form in form2:
	#				print(form.as_table())
	            	if form1.is_valid() and form2.is_valid():
	                    	try:
								if (create_content_type(form1.cleaned_data['content_type'],form2,form1.cleaned_data['is_leaf']) == False ):
									raise forms.ValidationError("something got wronged")
								new_obj = form1.save() #TODO many things
								print new_obj.content_type
	                    	except forms.ValidationError:
	                        		new_obj = None
	
	                    	if new_obj:
                        		return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            	(escape(new_obj._get_pk_val()), escape(new_obj)))
                    		else:
				        		page_context = {'form1': form1,'formset':form2,  'field': normal_model_name}
			            			return render_to_response('blogging/includes/add_content_type.html', page_context, context_instance=RequestContext(request))
            		else:
						print "form is not valid form1 ", form1.is_valid(), " form 2 ", form2.is_valid() 	
						page_context = {'form1': form1,'formset':form2,  'field': normal_model_name}
						return render_to_response('blogging/includes/add_content_type.html', page_context, context_instance=RequestContext(request))
		else:
			form = ContentTypeCreationForm()
			formset = FieldFormSet()
			print form.as_table()
	        page_context = {'form1': form,'formset':formset,  'field': normal_model_name }
        	return render_to_response('blogging/includes/add_content_type.html', page_context, context_instance=RequestContext(request))

def index(request):
#    output = 'Welcome to the section page !!!'
#    print "IP Address for debug-toolbar: " + request.META['REMOTE_ADDR']
#    output += " ".join(path)
#    print path
    template = loader.get_template('blogging/section.html')
    nodes = BlogParent.objects.all().filter(~Q(title='Orphan'),level=0)
    for node in nodes:
    	print 'printing nodes url ', node.get_absolute_url()
	
    context = RequestContext(request, {
										'parent': None,
                                       'nodes': nodes,
                                       'page': {'title':'Explore', 'tagline':'We learn from stolen stuff'},
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
		print "LOGS:: This is Detail page"
		blogs = BlogContent.objects.get(pk=post_id)
		template = loader.get_template('blogging/detail.html')
		content_class_name = find_class('blogging.'+blogs.content_type.__str__().lower(),blogs.content_type.__str__() )
		content_class = content_class_name()
		content_class.render_to_template(blogs)
		
		available_versions = reversion.get_for_object(blogs)
		patch_html = ""
		if len(available_versions) > 1 :
			old_version = available_versions[0]
			new_version = available_versions[1]
			patch_html = generate_diffs(old_version, new_version, "data",cleanup="semantic")
		context = RequestContext(request, {
										'parent': blogs.section.get_ancestors(include_self=True),		
                                       'nodes': blogs,
                                       'content':content_class,
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                       'patch': patch_html,
                                      })
		return HttpResponse(template.render(context))
	except ValueError:
		try:
			section = BlogParent.objects.get(slug = str(current_section))
		except :	
			return HttpResponse("Hi SomeThing Got Wrong!!! ")
		if section.is_leaf_node():
			template = loader.get_template('blogging/teaser.html')
			print "LOGS:: This is Leaf Node"
			nodes = BlogContent.published.filter(section=section)
			context = RequestContext(request, {
										'parent':section.get_ancestors(include_self=True),
                                       'nodes': nodes,
                                       'page': {'title':section.title, 'tagline':'We learn from stolen stuff'},
                                      })
			return HttpResponse(template.render(context))
		template = loader.get_template('blogging/section.html')
		print "LOGS:: This is NON Leaf Node"
		context = RequestContext(request, {
										'parent': section.get_ancestors(include_self=True),
                                       'nodes': section.get_descendants(),
                                       'page': {'title':section.title, 'tagline':'We learn from stolen stuff'},
                                      })
		return HttpResponse(template.render(context))
	
def ContactUs(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = 'Contact mail from PirateLearner'
			message = 'Name: ' + form.cleaned_data['name'] + '\n' + 'email: ' + form.cleaned_data['email'] + '\n Body: ' + form.cleaned_data['content']
			mail_admins(subject, message, fail_silently=False)
			template = loader.get_template('blogging/contact_success.html')
			context = RequestContext(request)
			return HttpResponse(template.render(context))
			print 'error during sending mail to Captain'
	else:
		form = ContactForm()
	return render_to_response('blogging/contact.html', {'example_form': form}, context_instance=RequestContext(request))