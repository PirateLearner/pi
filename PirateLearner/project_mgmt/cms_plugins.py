from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .utils import parse_feature
from project_mgmt import models

class MgmtPlugin(CMSPluginBase):

    module = 'ProjectManagement'

class WishlistPlugin(MgmtPlugin):
    render_template = 'project_mgmt/wishlistplugin.html'
    name = _(' Wishlist Plugin ')
    model = models.WishlistPlugin
    
    def render(self, context, instance, placeholder):
        request = context['request']
        feature_list = parse_feature()
        completed = []
        started = []
        pending = []
        for element in feature_list:
            if element['completed'] == 'YES':
                 completed.append(element)
            elif element['status'] != '0':
                 started.append(element)
            else:
                 pending.append(element)
        render_list = completed[0:instance.completed_number] + started[0:instance.started_number] + pending[0:instance.pending_number] 
        context.update({
                'features': render_list,
                'instance': instance,
        })

        return context
        
plugin_pool.register_plugin(WishlistPlugin)