from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from bookmarks import models
#from bookmarks.forms import LatestEntriesForm, SectionPluginForm, ContactForm

class BookmarksPlugin(CMSPluginBase):

    module = 'Bookmarks'




class LatestBookmarksPlugin(BookmarksPlugin):

    render_template = 'bookmarks/teaser_bookmark.html'
    name = _('Latest Bookmarks Entries')
    model = models.LatestBookmarksPlugin
#    form = LatestBookmarksForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(LatestBookmarksPlugin)
