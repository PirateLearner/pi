from copy import copy
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from django import template
from blogging.tag_lib import get_field_name_from_tag
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.mail import  mail_admins
from blogging.forms import ContactForm
from django.template import RequestContext
from bookmarks.models import Bookmark, BookmarkInstance, get_user_bookmark
import sys
import traceback

from django.conf import settings


register = template.Library()


class BookmarkRender(InclusionTag):
    template = 'bookmarks/templatetags/render_bookmarks.html'
    name = 'render_bookmark_pages'
    options = Options(
        Argument('user', default=None, required=False),
    )

    def __init__(self, parser, tokens):
        self.parser = parser
        super(BookmarkRender, self).__init__(parser, tokens)

    def get_template(self, context, **kwargs):
        return self.template

    def render_tag(self, context, **kwargs):
        """
        Overridden from InclusionTag to push / pop context to avoid leaks
        """
        context.push()
        print("render tag is called")
        try:
            template = self.get_template(context, **kwargs)
            data = self.get_context(context, **kwargs)
            output = render_to_string(template, data)
#             print(output)
            context.pop()
            return output
        except:
            print("Unexpected error:", sys.exc_info()[0])
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print("Error in %s on line %d" % (fname, lineno))

            return "Http404"


    def _get_data_context(self,context,user):
        extra_context = copy(context)
        if user:
            print("User ", user)
            if user == context['request'].user:
                extra_context['bookmarks'] =  BookmarkInstance.objects.filter(user=context['request'].user)
                print("Printing Bookmarks", extra_context['bookmarks'] )
            else:
                extra_context['bookmarks'] =  BookmarkInstance.objects.filter(user=context['request'].user,saved_instances__privacy_level = 'pub')
        else:
            extra_context['bookmarks'] =  Bookmark.objects.exclude(saved_instances__privacy_level = 'priv').order_by("-saved")
        return extra_context


    def get_context(self, context,user):
        extra_context = self._get_data_context(context, user)
        return extra_context

@register.simple_tag
def is_bookmarked(user,url):
    """
    Only to be used for intra site bookmarks
    """
#     domain = getattr(settings, 'DOMAIN_URL', None)
#     url = domain + url
    print("is_bookmarked: ", user , url)
    if get_user_bookmark(url,user):
        return True
    else:
        return False

@register.simple_tag
def get_promoted_bookmarks(num_entries):
    return BookmarkInstance.objects.all().filter(privacy_level='pub',is_promoted=True).order_by('-saved')[:num_entries]
register.tag(BookmarkRender)