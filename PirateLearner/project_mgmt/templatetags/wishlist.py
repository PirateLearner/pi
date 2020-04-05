from django import template
from project_mgmt.utils import parse_feature
from django.template.loader import get_template

from PirateLearner import settings

register = template.Library()

#Renderers

class WishlistNode(template.Node):
    def __init__(self):
        feature_list = parse_feature()
        completed = []
        started = []
        pending = []
        for element in feature_list:
            print((element['status'], element['completed']))
            if element['completed'] == 'YES':
                completed.append(element)
            elif element['status'] != '0':
                started.append(element)
            else:
                pending.append(element)

        self.render_list = pending[0:1] + started[0:2] + completed[0:2]

    def get_suggestion_url(self):
        #page = Page.objects.get(title='Contact Us') or None
        return (settings.DOMAIN_URL+'contact-us/?contact_type=Feature')

    def render(self, context):
        wishlistTemplate = get_template('project_mgmt/templatetags/wishlist/wishlist_sidebar.html')
        return wishlistTemplate.render(template.Context({'features': self.render_list,
                                                         'contact_url':self.get_suggestion_url()},
                                                        autoescape=context.autoescape))

#Compilation functions. These functions receive control and parameters from the template calls and are responsible for
#invoking and returning the rendered Nodes defined above as classes

@register.tag
def get_wishlist_list(parser, token):
    """
    Retrieves the wishlist elements from the file, as done in the normal view.
    """
    return WishlistNode()
