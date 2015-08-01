# Create your views here.

import datetime
import urllib2


from bookmarks.models import Bookmark, BookmarkFolderInstance, BookmarkInstance, get_user_bookmark, get_bookmark
from bookmarks import utils

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
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

def bookmarks(request):
    bookmarks = BookmarkInstance.objects.exclude(privacy_level = 'priv',user__is_staff=True).order_by("-saved")
    if request.user.is_authenticated():
        user_bookmarks = Bookmark.objects.filter(
            saved_instances__user=request.user
        )
    else:
        user_bookmarks = []
    return render_to_response("bookmarks/bookmarks.html", {
        "bookmarks": bookmarks,
        "user_bookmarks": user_bookmarks,
    }, context_instance=RequestContext(request))

def tagged_bookmarks(request,tag):
    try:
        bookmarks = BookmarkInstance.objects.filter(tags__name = tag)
        return render_to_response("bookmarks/bookmarks.html", {'bookmarks':bookmarks,} ,context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        raise Http404

@login_required
def your_bookmarks(request):
    bookmark_instances = BookmarkInstance.objects.filter(
        user=request.user
    ).order_by("-saved")
    return render_to_response("bookmarks/your_bookmarks.html", {
        "bookmark_instances": bookmark_instances,
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
                        initial = utils.fetch_bookmark(initial["url"])
                        if initial:
                            initial['message'] = "fetching successful!!!"
                            initial['message_type'] = "success" 
                            return HttpResponse(json.dumps(initial), content_type="application/json")
                        else:
                            initial = {}
                            initial['message'] = "Error in fetching !!!!"
                            initial['message_type'] = "danger"
                            return HttpResponse(json.dumps(initial), content_type="application/json")
            else:
                bookmark_form = BookmarkInstanceForm(request.user)
   
    return render_to_response("bookmarks/add.html", {
        "bookmark_form": bookmark_form,
    }, context_instance=RequestContext(request))


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
                    print "LOGS: bookamrk attributes: ", bookmark_instance.tags 
                    bookmark_instance.save(bookmark_instance.bookmark.url)
                    print "LOGS: tags to be saved are : ", bookmark_form.cleaned_data['tags']
                    bookmark_instance.tags.set(*bookmark_form.cleaned_data['tags'])
                    messages.success(request, _("You have updated bookmark '%(title)s'") % {
                            "title": bookmark_instance.title
                        })
                    return HttpResponseRedirect(reverse("bookmarks:all_bookmarks"))
            elif action == 'Delete':
                bookmark_instance.delete()
                messages.error(request, "Bookmark Deleted" )
                return HttpResponseRedirect(reverse("bookmarks:all_bookmarks"))
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
            meta = Meta(title = bookmark.title, description = truncatewords(description,120), section= bookmark.folder.title, url = bookmark.get_absolute_url(),
                    image = bookmark.get_image_url(), author = bookmark.user, date_time = bookmark.saved ,
                    object_type = 'article', keywords = [ tags.name for tags in bookmark.tags.all()])
            return render_to_response("bookmarks/detail.html", {'bookmark':bookmark,'meta':meta,} ,context_instance=RequestContext(request))

        except:
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
            return Http404
    except ValueError:
        print "Unexpected error invalid URL:", sys.exc_info()[0]
        return Http404
        








    


