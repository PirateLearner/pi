# Create your views here.
from django.dispatch import receiver
from django.template import RequestContext, loader
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
#from allauth.account.models import EmailAccount
from django.http import HttpResponseServerError
from django.urls import reverse
from taggit.models import Tag
from allauth.account.views import LoginView
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render_to_response

from core import utils
from core.forms import PreviewForm
import json
from core.plugins import ActionProvider

from django.contrib.auth.signals import user_logged_in

def details(request):
    """
    The main page that would be accessed by the user
    """
    preview_form = PreviewForm()
    plugins = [p for p in ActionProvider.plugins]
    return render_to_response("core/canvas.html", {'form':preview_form,'plugins':plugins }, context_instance=RequestContext(request))



def page_admin(request,page_slug=''):
    """
    admin page that would be dispayed either by default or by the URL core/page
    """



def page_create(request):
    """
    Page that accept the GET request from the Canvas Script
    """
#     print request
    if request.method == 'POST':
        post_data = request.POST.get('object_list')
        print(post_data)
        json_data = json.loads(post_data)
        try:
            name = json_data['name']
            print("LOGS: page create request is received with %(name)s" % {'name':name})
            obj_list  = json_data['obj_list']
            print("Object List is ", obj_list)
            plugin_array = []
            for elm in obj_list:
                plugin_obj = utils.plugins(elm['x'],elm['y'],elm['w'],elm['h'])
                plugin_array.append(plugin_obj)
            utils.create_array(plugin_array)
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        return HttpResponse("Got json data")

    else:
        print("Method is not POST")
        print(request.method)
        return HttpResponse("INVALID REQUEST")


