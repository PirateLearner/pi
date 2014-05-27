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
import os
from django.db.models import Q


# Create your views here.

class ContentWizard(SessionWizardView):
	def get_template_names(self):
		return "blogging/create_post.html"
	def get_form(self, step=None, data=None, files=None):
#		form = super(ContentWizard, self).get_form(step, data, files)
		# determine the step if not given
		form = None
		if step is None:
			step = self.steps.current
		print "this is step ", step
		if step == '0':
			form = ContentTypeForm() 
		if step == '1':
			data = self.get_cleaned_data_for_step('0') or {}
			content_type = data.get('ContentType')
			print type(content_type), content_type
			#content_type_class = content_type.lower()
			#from str(content_type_class)	import *
			form1 = find_class('blogging.'+content_type.__str__().lower(),str(content_type)+'Form' )	
			print type(form1), form1
			form = form1()
		return form

	def done(self, form_list, **kwargs):
		data = {}
        	for form in form_list:
            		data.update(form.cleaned_data)
		print data
		"""	
		content_type = data.get('ContentType')
		print type(content_type), content_type
		#content_type_class = content_type.lower()
		#from str(content_type_class)	import *
		wrapper_class = find_class('blogging.'+content_type.__str__().lower(),str(content_type))
		db_class = None
		if data['is_leaf'] == True:
			db_class = BlogContent()
			wrapper_class.render_to_db(db_class)
		else:
			db_class = BlogParent()
			wrapper_class.render_to_db(BlogParent)
		
		if db_class:
			db_class.save()	
		"""
		return HttpResponseRedirect('/')


@login_required
def content_type(request):
    if request.method == "POST":
        form = ContentTypeForm(request.POST)
        if form.is_valid():
            content_info = form['ContentType']
            request.session['content_info_id'] = content_info.id
            return HttpResponseRedirect(
                reverse("address_form"))
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
        "app/user_info.html",
        locals(), context_instance=RequestContext(request))	

@login_required
def add_new_model(request, model_name):
	if (model_name.lower() == model_name):
		normal_model_name = model_name.capitalize()
	else:
		normal_model_name = model_name
	print normal_model_name

	if normal_model_name == '0-ContentType' :
		FieldFormSet = formset_factory(FieldTypeForm,extra=2,max_num=2)
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
					
		        		page_context = {'form1': form1,'form2':form2,  'field': normal_model_name}
                			return render_to_response('blogging/includes/add_content_type.html', page_context, context_instance=RequestContext(request))
			else:
				print "form is not valid form1 ", form1.is_valid(), " form 2 ", form2.is_valid() 	
		        	page_context = {'form1': form1,'form2':form2,  'field': normal_model_name}
                		return render_to_response('blogging/includes/add_content_type.html', page_context, context_instance=RequestContext(request))
                else:
                 	form1 = ContentTypeCreationForm()
			form2 = FieldFormSet(initial= [
			{'field_name': 'title','field_type': 'Text'},
			])
			print form1.as_table()
			print form2
			for form in form2:
				print(form.as_table())
		        page_context = {'form1': form1,'form2':form2,  'field': normal_model_name}
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
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
    return HttpResponse(template.render(context))

@login_required
def new_page(request):
        if request.method == 'POST':
                form = PostEditForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
		    form.save()
                    return HttpResponseRedirect('/')
        else:
                form = PostEditForm(
                    initial={'title': 'Enter the page title'}
                )
                template = loader.get_template('blogging/create_page.html')
                context = RequestContext(request, {
                                               'form': form,
                                      })
                print form.media
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
		blogs = BlogContent.objects.get(pk=post_id)
		template = loader.get_template('blogging/detail.html')
                context = RequestContext(request, {
										'parent': blogs.section.get_ancestors(include_self=True),		
                                       'nodes': blogs,
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
			nodes = BlogContent.objects.all().filter(section=section)
			for node in nodes:
				node.data = strip_image_from_data(node.data)
				print 'after replace data is : ', node.data
			context = RequestContext(request, {
										'parent':section.get_ancestors(include_self=True),
                                       'nodes': nodes,
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
			return HttpResponse(template.render(context))
		template = loader.get_template('blogging/section.html')
		context = RequestContext(request, {
										'parent': section.get_ancestors(include_self=True),
                                       'nodes': section.get_descendants(),
                                       'page': {'title':'Pirate Learner', 'tagline':'We learn from stolen stuff'},
                                      })
		return HttpResponse(template.render(context))
	
