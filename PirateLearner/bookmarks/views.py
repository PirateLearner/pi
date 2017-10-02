# Create your views here.

import datetime
import urllib2


from bookmarks.models import Bookmark, BookmarkFolderInstance, BookmarkInstance, get_user_bookmark, get_bookmark
from bookmarks import utils

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
import json
from bookmarks.forms import BookmarkInstanceForm, BookmarkFolderForm,\
    BookmarkInstanceUpdateForm
from django.utils.html import escape, strip_tags
import traceback
from django.contrib.auth.decorators import permission_required
import sys
from django.core.exceptions import ObjectDoesNotExist
from meta_tags.views import Meta 
from blogging.utils import truncatewords
from bookmarks.utils import count_words

from bookmarks.serializers import BookmarkInstanceSerializer
from rest_framework import generics

from blogging.utils import group_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import length

from readability import Readability

def bookmarks(request):
    bookmarks = BookmarkInstance.objects.filter(is_promoted=True).exclude(privacy_level='priv').order_by("-saved")
#     if request.user.is_authenticated():
#         user_bookmarks = Bookmark.objects.filter(
#             saved_instances__user=request.user
#         )
#     else:
#         user_bookmarks = []
    return render_to_response("bookmarks/bookmarks.html", {
        "bookmarks": bookmarks,
        'result_title':'Bookmarks',
#         "user_bookmarks": user_bookmarks,
    }, context_instance=RequestContext(request))

def tagged_bookmarks(request,tag):
    try:
        bookmarks = BookmarkInstance.objects.filter(tags__slug = tag, is_promoted = True).exclude(privacy_level='priv')
        return render_to_response("bookmarks/bookmarks.html", {'bookmarks':bookmarks,} ,context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        raise Http404

@login_required
def your_bookmarks(request):
    bookmark_instances = BookmarkInstance.objects.filter(
        user=request.user
    ).order_by("-saved")
    return render_to_response("bookmarks/bookmarks.html", {
        "bookmarks": bookmark_instances,
        'result_title':'Bookmarks',
    }, context_instance=RequestContext(request))


@login_required
def add(request):
    if request.method == "POST":
        print "LOGS: ADD BOOKMARKS BY POST"
        bookmark_form = BookmarkInstanceForm(request.user, request.POST)
        if bookmark_form.is_valid():
            bookmark_instance = bookmark_form.save(commit=False)
            bookmark_instance.user = request.user
            bookmark_instance.save(bookmark_form.clean()['url'])
            bookmark_instance.tags.add(*bookmark_form.cleaned_data['tags'])
            messages.success(request, _("You have saved bookmark '%(title)s'") % {
                    "title": bookmark_instance.title
                })
            return HttpResponseRedirect(reverse("bookmarks:all_bookmarks"))
    else:
        initial = {}
        if request.method == "GET":
            if "url" in request.GET:
                print "LOGS: ADD BOOKMARKS BY GET URL %(url)s" % {'url':request.GET["url"]}
                initial["url"] = request.GET["url"]
                bookmark_instance = get_user_bookmark(initial["url"], request.user)
                if bookmark_instance:
                    initial['image_list'] = [bookmark_instance.image_url]
                    initial['title'] = bookmark_instance.title
                    initial['description'] = bookmark_instance.description
                else:
                    bookmark_instance = get_bookmark(initial["url"])
                    if bookmark_instance:
                        initial['image_list'] = [bookmark_instance.image_url]
                        initial['title'] = bookmark_instance.title
                        initial['description'] = bookmark_instance.description
                    else:
#                         initial = utils.fetch_bookmark(initial["url"])
                        initial = Readability(initial["url"]).parse()
                        if initial['content'] is not None:
                            initial['message'] = "fetching successful!!!"
                            initial['message_type'] = "success" 
                            return HttpResponse(json.dumps(initial), content_type="application/json")
                        else:
                            initial['message_type'] = "danger"
                            return HttpResponse(json.dumps(initial), content_type="application/json")
            else:
                bookmark_form = BookmarkInstanceForm(request.user)
   
    return render_to_response("bookmarks/add.html", {
        "form": bookmark_form,
    }, context_instance=RequestContext(request))

def snippet_testing(request):
    if request.method == "GET":
        if "url" in request.GET:
            initial = {}
            initial["url"] = request.GET["url"]
            initial = Readability(initial["url"]).parse()
            return render_to_response("bookmarks/snippet_test.html", {
        "data": initial,
    }, context_instance=RequestContext(request))
        else:
            raise HttpResponseBadRequest
    else:
        raise HttpResponseBadRequest

@permission_required('bookmarks.change_bookmarks','bookmarks.delete_bookmarks')
def update(request, bookmark_instance_id):

    bookmark_instance = get_object_or_404(
        BookmarkInstance,
        pk=bookmark_instance_id
    )

    try:
        if request.method == "POST":
            action = request.POST.get('submit')
            if action == 'Update':
                print "LOGS: ADD BOOKMARKS BY POST"
                bookmark_form = BookmarkInstanceUpdateForm(bookmark_instance.user,bookmark_instance_id,request.POST)
                if bookmark_form.is_valid():
                    bookmark_instance = bookmark_form.save(commit=False)
                    print "LOGS: bookamrk attributes: ", bookmark_instance.bookmark.url
                    print "LOGS: bookamrk attributes: ", bookmark_instance.title
                    print "LOGS: bookamrk attributes: ", bookmark_instance.description
                    print "LOGS: bookamrk attributes: ", bookmark_instance.note
                    print "LOGS: bookamrk attributes: ", bookmark_instance.privacy_level
                    content = Readability(bookmark_instance.bookmark.url).parse()
                    if content['content'] is not None:
                        bookmark_instance.description = content['content']
                    bookmark_instance.save(bookmark_instance.bookmark.url)
                    print "LOGS: tags to be saved are : ", bookmark_form.cleaned_data['tags']
                    bookmark_instance.tags.set(*bookmark_form.cleaned_data['tags'])
                    messages.success(request, _("You have updated bookmark '%(title)s'") % {
                            "title": bookmark_instance.title
                        })
                    return HttpResponseRedirect(reverse("bookmarks:all_bookmarks"))
                else:
                    return render_to_response("bookmarks/update.html", 
                                              {"bookmark_form": bookmark_form,}, 
                                              context_instance=RequestContext(request))
            elif action == 'Delete':
                bookmark_instance.delete()
                messages.error(request, "Bookmark Deleted" )
                return HttpResponseRedirect(reverse("bookmarks:all_bookmarks"))
            else:
                return HttpResponseBadRequest
        else:
            initial = {
                       "folder":bookmark_instance.folder,
                       "title": bookmark_instance.title,
                       "description":str(bookmark_instance.description),
                       "note":bookmark_instance.note,
                       "privacy_level":bookmark_instance.privacy_level,
                       "tags":bookmark_instance.tags.all(), 
                       
                       }
            bookmark_form = BookmarkInstanceUpdateForm(bookmark_instance.user,bookmark_instance_id,initial = initial)
        return render_to_response("bookmarks/update.html", {"bookmark_form": bookmark_form,}, context_instance=RequestContext(request))
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
        raise Http404






@login_required
def add_folder(request,model_name):
    if (model_name.lower() == model_name):
        normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name
    if normal_model_name == 'Folder' :
        if request.method == "POST":
            bookmark_form = BookmarkFolderForm(request.user, request.POST)
            if bookmark_form.is_valid():
                bookmark_instance = bookmark_form.save(commit=False)
                bookmark_instance.adder = request.user
                bookmark_instance.save()
                messages.success(request, _("You have saved folder '%(title)s'") % {
                        "title": bookmark_instance.title
                    })
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                    (escape(bookmark_instance._get_pk_val()), escape(bookmark_instance)))
            else:
                page_context = {'form': bookmark_form,  'field': normal_model_name }
                return render_to_response('bookmarks/add_folder.html', page_context, context_instance=RequestContext(request))
            
        else:
            bookmark_form = BookmarkFolderForm(request.user, request.POST)
            page_context = {'form': bookmark_form,  'field': normal_model_name }
            return render_to_response('bookmarks/add_folder.html', page_context, context_instance=RequestContext(request))
            
    



def bookmark_details(request,slug):
    current_section = slug.split("/")[-1]
#     print current_section
    try:
        post_id = int(current_section)
        print "LOGS:: This is Detail page of bookmarks"
        try:
            bookmark = BookmarkInstance.objects.get(pk=post_id)
            description = strip_tags(bookmark.note)
            if count_words(description)<5:
                description = bookmark.description
            meta = Meta(title = bookmark.title, description = bookmark.get_summary(), section= bookmark.folder.title, url = bookmark.get_absolute_url(),
                    image = bookmark.get_image_url(), author = bookmark.user, date_time = bookmark.saved ,
                    object_type = 'article', keywords = [ tags.name for tags in bookmark.tags.all()])
            if request.user.is_authenticated():
                can_edit = (request.user.is_staff == True) or request.user == bookmark.user 
            else:
                can_edit = False 
            return render_to_response("bookmarks/detail.html", {'bookmark':bookmark,'meta':meta,'can_edit':can_edit } ,context_instance=RequestContext(request))

        except:
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
            raise Http404
    except ValueError:
        print "Unexpected error invalid URL:", sys.exc_info()[0]
        raise Http404
        
@group_required('Administrator')
def manage(request):
    """
    Manage the bookmarks; only available to administrators
    """
     # Check the parameters passed in the URL and process accordingly
    action = request.GET.get('action', None)
    bookmark_ids = request.GET.get('ids', None)    

    if request.is_ajax() and request.method == "POST":
        if action is None or bookmark_ids is None:
            print "Error: manage: No parameter(s) passed."
            res = {}
            res['result'] = 'failure'
            res['return_text'] = 'No parameter(s) passed'
            return JsonResponse(res)
        bookmark_ids = [x.strip() for x in bookmark_ids.split(',')]
        # remove comma from the 
        if not bookmark_ids[-1]:
            bookmark_ids = bookmark_ids[:-1]
        action = action.strip()
        print "manage: action=", action, "bookmarks=", bookmark_ids
        count = 0
        try:
            if len(bookmark_ids):
                res = {}
                objs = BookmarkInstance.objects.filter(pk__in=bookmark_ids)
                
                if action == 'Promote':
                    print "LOGS: Promote the given bookmarks"
                    obj_errors = []
                    obj_published = []
                    for obj in objs:
                        if obj.privacy_level == "pub":
                            obj.is_promoted = True
                            obj.save(obj.bookmark.url)
                            obj_published.append(obj.id)
                            count += 1
                        else:
                            obj_errors.append('Bookmark "{obj}" is private. Could not promote'.format(obj=obj))
                    res['return_text'] = '{count} bookmarks promoted sucessfully!!'.format(count=count)
                    res['result'] = 'success'
                    res['published_id'] = obj_published
                    res['action'] = "Publish"
                    if len(obj_errors) > 0:
                        res['return_text'] += '\n'
                        res['return_text'] += '\n'.join(obj_errors)
                        res['result'] = 'failure'
                elif action == 'Delete':
                    for obj in objs:
                        obj.delete()
                        count += 1
                    res['return_text'] = '{count} bookmarks deleted sucessfully!!'.format(count=count)
                    res['result'] = 'success'
                    res['action'] = "Delete"

                elif action == "Demote":
                    print "LOGS: Promote the given bookmarks"
                    obj_published = []
                    for obj in objs:
                        obj.is_promoted = False
                        obj.save(obj.bookmark.url)
                        obj_published.append(obj.id)
                        count += 1
                    res['return_text'] = '{count} bookmarks unpublished sucessfully!!'.format(count=count)
                    res['result'] = 'success'
                    res['published_id'] = obj_published
                    res['action'] = "Unpublish"

                elif action == "Make public":
                    print "LOGS: Promote the given bookmarks"
                    obj_errors = []
                    obj_published = []
                    for obj in objs:
                        if obj.user == request.user:
                            obj.privacy_level = "pub"
                            obj.save(obj.bookmark.url)
                            obj_published.append(obj.id)
                            count += 1
                        else:
                            obj_errors.append('Bookmark "{obj}" is not you creation!!!'.format(obj=obj))
                    res['return_text'] = '{count} bookmarks make public sucessfully!!'.format(count=count)
                    res['result'] = 'success'
                    res['published_id'] = obj_published
                    res['action'] = "Public"
                    if len(obj_errors) > 0:
                        res['return_text'] += '\n'
                        res['return_text'] += '\n'.join(obj_errors)
                        res['result'] = 'failure'

                elif action == "Make private":
                    print "LOGS: Promote the given bookmarks"
                    obj_errors = []
                    obj_published = []

                    for obj in objs:
                        if obj.user == request.user:                        
                            obj.privacy_level = "priv"
                            obj.save(obj.bookmark.url)
                            obj_published.append(obj.id)
                            count += 1
                        else:
                            obj_errors.append('Bookmark "{obj}" is not you creation!!!'.format(obj=obj))
                    res['return_text'] = '{count} bookmarks make public sucessfully!!'.format(count=count)
                    res['result'] = 'success'
                    res['published_id'] = obj_published
                    res['action'] = "Private"
                    if len(obj_errors) > 0:
                        res['return_text'] += '\n'
                        res['return_text'] += '\n'.join(obj_errors)
                        res['result'] = 'failure'
                print "manage_articles: Total", count
                return JsonResponse(res)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
            res = {}
            res['result'] = 'error'
            return JsonResponse(res) 

    page = request.GET.get('page',None)
    tab = request.GET.get('tab','all')
    try:
        if request.user.is_staff:
            base_queryset = BookmarkInstance.objects.all()
        else:
            base_queryset = BookmarkInstance.objects.all(user=request.user)

        if tab == "all":
            bookmarks = base_queryset
            result_title = 'all bookmarks'
        elif tab == "promoted":
            bookmarks = base_queryset.filter(is_promoted=True)
            result_title = 'promoted bookmarks'
        elif tab == "public":
            bookmarks = base_queryset.filter(privacy_level="pub")
            result_title = 'public bookmarks'
        elif tab == "private":
            bookmarks = base_queryset.filter(privacy_level="priv")
            result_title = 'private bookmarks'
        else:
            bookmarks = base_queryset
            result_title = 'all bookmarks'

        
        paginator = Paginator(bookmarks, 50,orphans=30)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pages = paginator.page(paginator.num_pages)
        actions = [{"name":"Delete", "help":"Delete selected bookmarks"},
                   {"name":"Promote", "help":"Promote selected bookmarks"},
                   {"name":"Demote", "help":"Demote selected bookmarks"},
                   {"name":"Make public", "help":"set visibility as public bookmark"},
                   {"name":"Make private", "help":"set visibility as private bookmark"},
                   ]
        tab_css_class = ['is-active']
        query_tabs = [ 
                    {     'name': 'All', 
                        'url': reverse("bookmarks:manage_bookmarks")+'?tab=all', 
                        'css': ' '.join(tab_css_class) if tab == 'all' else '',
                        'help_text': 'List of all bookmarks.'
                    },
                    {     'name': 'Promoted', 
                        'url': reverse("bookmarks:manage_bookmarks")+'?tab=promoted', 
                        'css': ' '.join(tab_css_class) if tab == 'promoted' else '',
                        'help_text': 'List of all promoted bookmarks.'
                    },
                    {     'name': 'Public', 
                        'url': reverse("bookmarks:manage_bookmarks")+'?tab=public', 
                        'css':  ' '.join(tab_css_class) if tab == 'public' else '',
                        'help_text': 'List of public bookmarks.'
                    },
                    {     'name': 'Private', 
                        'url': reverse("bookmarks:manage_bookmarks")+'?tab=private', 
                        'css': ' '.join(tab_css_class) if tab == 'private' else '',
                        'help_text': 'List of private bookmarks.'
                    }
                    ]
        
        template = loader.get_template('bookmarks/manage.html')
        context = {"bookmarks": pages, "actions": actions, 'query_tabs':query_tabs,'result_title':result_title
                   }
        return HttpResponse(template.render(context,request))
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
        raise Http404
    





    


