
from copy import copy
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from django import template
from blogging.tag_lib import get_field_name_from_tag
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from dashboard.models import UserProfile
import sys
import traceback

register = template.Library()

class SocialProfile(InclusionTag):
    template = 'dashboard/templatetags/social_profile.html'
    name = 'social_profile'
    options = Options(
        Argument('provider'),
        Argument('userid', default=None, required=False),
    )

    def __init__(self, parser, tokens):
        self.parser = parser
        super(SocialProfile, self).__init__(parser, tokens)
        
    def get_template(self, context, **kwargs):
        return self.template
    
    def render_tag(self, context, **kwargs):
        """
        Overridden from InclusionTag to push / pop context to avoid leaks
        """
        context.push()
        print "LOGS: social profile tag is called"
        try:
            template = self.get_template(context, **kwargs)
            data = self.get_context(context, **kwargs)
            output = render_to_string(template, data)
#             print output
            context.pop()
            return output
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return "Http404"

        
    def _get_data_context(self,context,provider,userid):
        extra_context = copy(context)
        print "LOGS: _get_data_context called "
        if userid:
            print "atrribute ", userid
            try:
                profile = UserProfile.objects.get(user = userid)
            except UserProfile.DoesNotExist:
                print "LOGS: User Does Not exist"
                return extra_context        
        else:
            try:
                profile = UserProfile.objects.get(user = extra_context["request"].user)
                print "LOGS: _get_data_context--> profile  ", profile
            except UserProfile.DoesNotExist:
                print "LOGS: User Does Not exist"
                return extra_context        
            
        try:
            if profile.is_social_account_exist(provider):
                extra_context['provider_name'] = profile.get_provider_name(provider)
                extra_context['profile_image'] = profile.get_avatar_url(provider)
                extra_context['profile_username'] = profile.get_name(provider)
                extra_context['profile_gender'] = profile.get_gender(provider)
                extra_context['profile_url'] = profile.get_social_url(provider)
                extra_context['profile_email'] = profile.get_email(provider)
            else:
                extra_context['profile_disable'] = True
                extra_context['provider_name'] = provider
                extra_context['profile_username'] = profile.get_name(provider)
                extra_context['profile_image'] = profile.get_avatar_url(provider)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
        return extra_context
            

    def get_context(self, context,provider, userid=None):
        """
        provider is required, if userid is not provided then use current logged-in user.
        """
        extra_context = self._get_data_context(context, provider, userid)
        return extra_context

register.tag(SocialProfile)