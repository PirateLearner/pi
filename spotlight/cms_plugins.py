from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from spotlight import models
from spotlight.forms import LatestSpotlightForm

class SpotlightPlugin(CMSPluginBase):

    module = 'Spotlight'




class LatestSpotlightPlugin(SpotlightPlugin):

    render_template = 'spotlight/spotlight_plugin.html'
    name = _('Latest Spotlight Entries')
    model = models.LatestSpotlightPlugin
    form = LatestSpotlightForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(LatestSpotlightPlugin)
