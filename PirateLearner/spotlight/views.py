# Create your views here.



from spotlight.models import Spotlight, TYPE
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from spotlight.forms import SpotlightForm
from blogging.models import BlogContent
from bookmarks.models import BookmarkInstance
import re
import traceback
from django.contrib.auth.decorators import permission_required
import sys
from django.core.exceptions import ObjectDoesNotExist, ValidationError


def index(request):
    featured_posts = Spotlight.objects.all().order_by("-added")
    print("LOGS: index SPOTLIGHT", featured_posts)
    featured_list = []

    for post in featured_posts:
        tmp = {}
        tmp['type'] = dict(TYPE)[post.type]
        tmp['object'] = post.content_object
        featured_list.append(tmp)

<<<<<<< HEAD
    return render(request, "spotlight/index.html", {
=======
    return render(request,"spotlight/index.html", {
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62
        "featured_posts": featured_list,
    })

def tagged_spotlight(request,tag):
    try:
        featured_posts = Spotlight.objects.all().order_by("-added")

        featured_list = []

        for post in featured_posts:
            if tag in post.content_object.get_tags():
                tmp = {}
                tmp['type'] = dict(TYPE)[post.type]
                tmp['object'] = post.content_object
                featured_list.append(tmp)
<<<<<<< HEAD
        return render(request, "spotlight/index.html", {'featured_posts':featured_list,})
=======
        return render(request,"spotlight/index.html", {'featured_posts':featured_list,} ,context_instance=RequestContext(request))
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62
    except ObjectDoesNotExist:
        raise Http404

def featured(request):
    featured_posts = Spotlight.objects.all().order_by("-added")

    featured_list = []

    for post in featured_posts:
        if 0 == post.type:
            tmp = {}
            tmp['type'] = dict(TYPE)[post.type]
            tmp['object'] = post.content_object
            featured_list.append(tmp)
    return render(request,"spotlight/index.html", {
        "featured_posts": featured_list,
    })

def promoted(request):
    featured_posts = Spotlight.objects.all().order_by("-added")

    featured_list = []

    for post in featured_posts:
        if 1 == post.type:
            tmp = {}
            tmp['type'] = post.type
            tmp['object'] = post.content_object
            featured_list.append(tmp)
<<<<<<< HEAD
    return render(request, "spotlight/index.html", {
=======
    return render(request,"spotlight/index.html", {
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62
        "featured_posts": featured_list,
    })



@login_required
def add_spotlight(request):

    if request.method == "POST":
        print("LOGS: ADD SPOTLIGHT BY POST")
        spotlight_form = SpotlightForm(request.POST)

        app_map = {'C': 'blogging', 'bookmarks': 'bookmarks'}

        if spotlight_form.is_valid():
            spotlight_instance = Spotlight()
            spotlight_instance.adder = request.user
            spotlight_instance.type = spotlight_form.clean()['type']
            site_name = get_current_site(request)
            print("LOGS:", site_name)
            pattern = r'^.*%(site)s/(\w+)/(\w*)/.+/([0-9]+)/?/'% {'site':site_name}
            print("LOGS:", pattern)
            print("LOGS:", spotlight_form.clean()['url'])
            match = re.search(pattern, spotlight_form.clean()['url'])
            print("LOGS:", match)
            if match:
                print("LOGS: app ", match.group(2), app_map[match.group(2)])
                print("LOGS: id ", match.group(3))
                app_name = app_map[match.group(2)]
                post_id = int(match.group(3))
                if app_name == 'blogging':
                    post = BlogContent.objects.get(pk=post_id)
                elif app_name == 'bookmarks':
                    post = BookmarkInstance.objects.get(pk=post_id)
                spotlight_instance.content_object = post
                spotlight_instance.save()
                messages.success(request, _("'%(title)s' has been flagged") % {
                    "title": post.get_title()
                })
                return HttpResponseRedirect(reverse("spotlight:all_spotlight"))
            else:
                ValidationError(_('Invalid URL'), code='invalid')
        else:
            print("LOGS: form is not valid ", spotlight_form.errors)
    else:
        spotlight_form = SpotlightForm(request.POST)
<<<<<<< HEAD
    return render(request, "spotlight/add.html", {
=======
    return render(request,"spotlight/add.html", {
>>>>>>> e8b002fcfc6266dc0413bb189eda4781137a2a62
        "spotlight_form": spotlight_form,
    })


@permission_required('spotlight.change_bookmarks','spotlight.delete_bookmarks')
def delete_spotlight(request, spotlight_instance_id):

    spotlight_instance = get_object_or_404(
        Spotlight,
        pk=spotlight_instance_id
    )

    try:
        spotlight_instance.delete()
        messages.error(request, "Spotlight Deleted" )
        return HttpResponseRedirect(reverse("spotlight:all_spotlight"))

    except:
        print("Unexpected error:", sys.exc_info()[0])
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print("Error in %s on line %d" % (fname, lineno))
        return Http404



















