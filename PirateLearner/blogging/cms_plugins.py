from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from blogging import models
from blogging.forms import LatestEntriesForm, SectionPluginForm

class BlogPlugin(CMSPluginBase):

    module = 'Blogging'


class LatestEntriesPlugin(BlogPlugin):

    render_template = 'blogging/plugin/plugin_teaser.html'
    name = _('Latest Blog Entries')
    model = models.LatestEntriesPlugin
    form = LatestEntriesForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
#	context['nodes'] = self.model.get_post()
        return context

class SectionPlugin(BlogPlugin):
    render_template = 'blogging/plugin/plugin_section.html'
    name = _(' Blog Section Plugin ')
    model = models.SectionPlugin
    form = SectionPluginForm

plugin_pool.register_plugin(LatestEntriesPlugin)
plugin_pool.register_plugin(SectionPlugin)


