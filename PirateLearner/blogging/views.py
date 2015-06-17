"""@package PirateDocs 
	This is main view module for Blogging app supporting various view provided to the User.
"""

import sys
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render_to_response, render
from django.contrib import auth
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect, Http404
from blogging.models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blogging.forms import *
from blogging.create_class import CreateClass
from django.contrib.formtools.wizard.views import SessionWizardView
from django.forms.formsets import formset_factory
from django.utils.html import escape
from blogging.utils import *
from blogging.wrapper import *
import os, errno
from django.db.models import Q
from django.core.mail import send_mail, mail_admins
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import reversion
from reversion.helpers import generate_diffs

from meta_tags.views import Meta 
from blogging.utils import strip_image_from_data
from blogging.tag_lib import strip_tag_from_data
from blogging.utils import trucncatewords,slugify_name
from django.utils.html import strip_tags

import traceback
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from blogging.db_migrate import migrate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
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
					filename = os.path.abspath(os.path.dirname(__file__))+"/custom/"+content_info.__str__().lower()+".py"
					os.remove(filename)
					filename = os.path.abspath(os.path.dirname(__file__))+"/templates/blogging/includes/"+content_info.__str__().lower()+".html"
					os.remove(filename)
					content_info.delete()
				except OSError as e: # this would be "except OSError, e:" before Python 2.6
					raise # re-raise exception if a different error occured
	else:
		if 'content_info_id' in request.session:
			try:
				content_info_obj = BlogContentType.objects.get(
	                id=request.session['content_info_id']
	            )
				data = { 'ContentType':content_info_obj	}
				form = ContentTypeForm(initial=data)
			except ObjectDoesNotExist:
				del request.session['content_info_id']
				form = ContentTypeForm()
		else:
			form = ContentTypeForm()
	return render_to_response(
	    "blogging/content_type.html",
	    locals(), context_instance=RequestContext(request))	

class ContentTypeFormView(View):

	form_class = ContentTypeForm
	template_name = 'blogging/content_type.html'

	def get(self, request, *args, **kwargs):
		if 'content_info_id' in request.session:
			try:
				content_info_obj = BlogContentType.objects.get(
		            id=request.session['content_info_id']
		        )
				data = { 'ContentType':content_info_obj	}
				form = self.form_class(initial=data)
			except ObjectDoesNotExist:
				del request.session['content_info_id']
				form = self.form_class()
		else:
			form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			# <process form cleaned data>
			action = request.POST.get('submit')
			content_info = form.cleaned_data['ContentType']

			if action == 'next':
				print content_info, type(content_info)
				request.session['content_info_id'] = content_info.id
				return HttpResponseRedirect(
		            reverse("blogging:create-post"))
			if action == 'delete':
				try:
					filename = os.path.abspath(os.path.dirname(__file__))+"/custom/"+content_info.__str__().lower()+".py"
					os.remove(filename)
					content_info.delete()
				except OSError as e: # this would be "except OSError, e:" before Python 2.6
					if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
						raise # re-raise exception if a different error occured

		return render(request, self.template_name, {'form': form})



@login_required
def new_post(request):
	"""
	Used for creating new post depending upon the content type chosen by the user in previous step.
	If content type is not selected then redirect to content-type page for selection of appropriate content type.
	Operations:
	BACK -- Go back to previous step for selecting new content type.
	SAVE -- Save the content as draft for later revision. todo:

	SUBMIT -- Submit the post for moderation and publication. 
	"""
	if 'content_info_id' not in request.session:
		return HttpResponseRedirect(reverse("blogging:content-type"))

	content_info_obj = BlogContentType.objects.get(
	        id=request.session['content_info_id']
    )
	print request.session['content_info_id'], content_info_obj
	form = find_class('blogging.custom.'+content_info_obj.__str__().lower(),str(content_info_obj).capitalize()+'Form' )

	if request.method == "POST":
		post_form = form(reverse('blogging:create-post'),request.POST)
		
		if post_form.is_valid():
			post = request.POST.copy()
			if content_info_obj.is_leaf:
				blog = BlogContent()
				blog.section = post_form.cleaned_data["section"]
			else:
				blog = BlogParent()
				blog.parent = post_form.cleaned_data["parent"]
			blog.title = post_form.cleaned_data["title"]
			blog.author_id = request.user
			blog.content_type = content_info_obj
			blog.slug = slugify(blog.title)
			blog.data = post_form.save(post)
			blog.save()
			if content_info_obj.is_leaf:
				blog.tags.add(*post_form.cleaned_data['tags'])
			del request.session['content_info_id']
			return HttpResponseRedirect(blog.get_absolute_url())
# 			return render_to_response(
# 									"blogging/create_page.html",
# 	    				context, context_instance=RequestContext(request))

	else:
		initial = {'pid_count': '0'}
		post_form = form(reverse('blogging:create-post'),initial=initial)
	context = {'form':post_form}
	return render_to_response(
	    "blogging/create_page.html",
	    context, context_instance=RequestContext(request))

@login_required
def edit_post(request,post_id):
	"""
	Used for editing existing post depending upon the post_id in the request.
	SAVE -- Save the content as draft for later revision. todo:
	SUBMIT -- Submit the post for moderation and publication. 
	"""
	
	try:
		blog = BlogContent.objects.get(pk=post_id)
		request.session['content_info_id'] = blog.content_type.id
		print "LOGS: EDIT ", blog.__str__()
		form = find_class('blogging.custom.'+blog.content_type.__str__().lower(),str(blog.content_type).capitalize()+'Form' )
		print "LOGS: ContentType ", blog.content_type.__str__().lower()
		if request.method == "POST":
			post_form = form(reverse('blogging:edit-post',args = (post_id,)),request.POST)
			
			if post_form.is_valid():
				post = request.POST.copy()
				blog.title = post_form.cleaned_data["title"]
				blog.section = post_form.cleaned_data["section"]
				blog.author_id = request.user
				blog.slug = slugify(blog.title)
				blog.data = post_form.save(post)
				blog.save()
				blog.tags.set(*post_form.cleaned_data['tags'])				
				return HttpResponseRedirect(blog.get_absolute_url())
# 				return render_to_response(
# 										"blogging/create_page.html",
# 		    				context, context_instance=RequestContext(request))

		else:
			wrapper_form_class = find_class('blogging.custom.'+blog.content_type.__str__().lower(),str(blog.content_type).capitalize()+'Form')
			print "LOGS: Wrapper Form Class ", wrapper_form_class
			print "LOGS: Content Class ", blog
			json_obj = json.loads(blog.data)
			print json_obj
			json_obj['title'] = blog.title
			json_obj['section'] = blog.section
			json_obj['tags'] = blog.tags.all()
			post_form = wrapper_form_class(reverse('blogging:edit-post',args = (post_id,)),initial=json_obj)

		context = {'form':post_form}
		return render_to_response(
		    "blogging/create_page.html",
		    context, context_instance=RequestContext(request))	
	except:
		print "Unexpected error:", sys.exc_info()[0]
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			print "Error in %s on line %d" % (fname, lineno)
		raise Http404


@login_required
def add_new_model(request, model_name):
	if (model_name.lower() == model_name):
		normal_model_name = model_name.capitalize()
	else:
		normal_model_name = model_name
	print normal_model_name
	
	if normal_model_name == 'ContentType' :
		FieldFormSet = formset_factory(FieldTypeForm,extra=1)
		if request.method == 'POST':
			form1 = ContentTypeCreationForm(request.POST)
			form2 = FieldFormSet(request.POST)
			if form1.is_valid() and form2.is_valid():
				try:
					form_dict = {}
					for form in form2:
						form_dict[form.cleaned_data['field_name']] = form.cleaned_data['field_type']
					print "LOGS: Printing fomr dictionary: ", form_dict 
						
					
					if (create_content_type(slugify_name(form1.cleaned_data['content_type']),form_dict,form1.cleaned_data['is_leaf']) == False ):
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
	template = loader.get_template('blogging/section.html')
	nodes = BlogParent.objects.all().filter(~Q(title='Orphan'),level=0)
	max_entry = getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 3)
	paginator = Paginator(nodes, max_entry,orphans=3)
	page = request.GET.get('page')
	try:
		pages = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		pages = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		pages = paginator.page(paginator.num_pages)

	
	print "Index page is call"
	context = RequestContext(request, {
										'parent': None,
                                       'nodes': pages,
                                       'page': {'title':'Explore', 'tagline':'We learn from stolen stuff'},
                                       'max_entry': max_entry,
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
	print  "Printing slug ", slug
	if len(slug) == 0:
		return  ""
	try:
		post_id = int(current_section)
		print "LOGS:: This is Detail page"
		if request.GET.get('edit',None) == 'True':
			return HttpResponseRedirect(reverse('blogging:edit-post',args = (post_id,)))
		try:
			blogs = BlogContent.objects.get(pk=post_id)
		except BlogContent.DoesNotExist:
			raise Http404
		template = loader.get_template('blogging/includes/'+ blogs.content_type.__str__().lower() + '.html')
		try:
			json_obj = json.loads(blogs.data)
			json_obj['title'] = blogs.title
			json_obj['edit'] = reverse('blogging:edit-post',args = (post_id,))
			# Instantiate the Meta class
			description = strip_tags(json_obj.values()[0])
			meta = Meta(title = blogs.title, description = trucncatewords(description,120), section= blogs.section.title, url = blogs.get_absolute_url(),
					image = blogs.get_image_url(), author = blogs.author_id, date_time = blogs.publication_start ,
					object_type = 'article', keywords = [ tags.name for tags in blogs.tags.all()])
			
			available_versions = reversion.get_for_object(blogs)
			patch_html = ""
			if len(available_versions) > 1 :
				old_version = available_versions[0]
				new_version = available_versions[1]
				patch_html = generate_diffs(old_version, new_version, "data",cleanup="semantic")
		except:
			print "Unexpected error:", sys.exc_info()[0]
			for frame in traceback.extract_tb(sys.exc_info()[2]):
				fname,lineno,fn,text = frame
				print "Error in %s on line %d" % (fname, lineno)
			raise Http404

		context = RequestContext(request, {
										'parent': blogs.section.get_ancestors(include_self=True),		
                                       'nodes': blogs,
                                       'content':json_obj,
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                       'patch': patch_html,
                                       'meta' : meta,
                                      })
		return HttpResponse(template.render(context))
	except (ValueError):
		try:
			section = BlogParent.objects.get(slug = str(current_section))
		except (BlogParent.DoesNotExist):	
			print "Unexpected error:", sys.exc_info()[0]
			for frame in traceback.extract_tb(sys.exc_info()[2]):
				fname,lineno,fn,text = frame
				print "Error in %s on line %d" % (fname, lineno)
			raise Http404
		
		max_entry = getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 3)

		if section.is_leaf_node():
			template = loader.get_template('blogging/teaser.html')
			print "LOGS:: This is Leaf Node"
			nodes = BlogContent.published.filter(section=section)
			paginator = Paginator(nodes, max_entry,orphans=3)
			page = request.GET.get('page')
			try:
				pages = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				pages = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				pages = paginator.page(paginator.num_pages,orphans=3)
			context = RequestContext(request, {
										'parent':section.get_ancestors(include_self=True),
                                       'nodes': pages,
                                       'page': {'title':section.title, 'tagline':'We learn from stolen stuff'},
                                       'max_entry': max_entry,
                                      })
			return HttpResponse(template.render(context))
		template = loader.get_template('blogging/section.html')
		print "LOGS:: This is NON Leaf Node ", section.get_children()
		paginator = Paginator(section.get_children(), max_entry)
		page = request.GET.get('page')
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)
		context = RequestContext(request, {
										'parent': section.get_ancestors(include_self=True),
                                       'nodes': pages,
                                       'page': {'title':section.title, 'tagline':'We learn from stolen stuff'},
                                       'max_entry': max_entry,
                                      })
		return HttpResponse(template.render(context))

def tagged_post(request,tag):
	try:
		posts = BlogContent.objects.filter(tags__name = tag)
		max_entry = getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 3)
		
		page = request.GET.get('page')
		paginator = Paginator(posts, max_entry)
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)

		template = loader.get_template('blogging/teaser.html')
		context = RequestContext(request, {
                                       'nodes': pages,
                                       'page': {'title':tag, 'tagline':'We learn from stolen stuff'},
                                       'max_entry': max_entry,
                                      })
		return HttpResponse(template.render(context))
	except ObjectDoesNotExist:
		raise Http404

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


def testCase(request):
	try:
		migrate()
		return render_to_response('blogging/Test_page.html', {}, context_instance=RequestContext(request))
	except:
		print "Unexpected error:", sys.exc_info()[0]
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			print "Error in %s on line %d" % (fname, lineno)
		raise Http404
	

