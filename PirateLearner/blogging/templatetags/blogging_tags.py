
from copy import copy
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from django import template
from blogging.tag_lib import get_field_name_from_tag
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

class ContentRender(InclusionTag):
    template = 'blogging/templatetags/render_content.html'
    name = 'render_content'
    options = Options(
        Argument('instance'),
        Argument('attribute', default=None, required=False),
    )

    def __init__(self, parser, tokens):
        self.parser = parser
        super(ContentRender, self).__init__(parser, tokens)
        
    def get_template(self, context, **kwargs):
        return self.template
    
    def render_tag(self, context, **kwargs):
        """
        Overridden from InclusionTag to push / pop context to avoid leaks
        """
        context.push()
        print "render tag is called"
        template = self.get_template(context, **kwargs)
        data = self.get_context(context, **kwargs)
        output = render_to_string(template, data)
        print output
        context.pop()
        return output

        
    def _get_data_context(self,context,instance,attribute):
        extra_context = copy(context)
        if attribute:
            print "atrribute ", attribute
            extra_context['attribute_name'] = attribute.__str__()
            extra_context['attribute'] = getattr(instance, attribute, '')
        else:
            print "tag list ", instance.tag_list
            attribute_list = []
            for tag in instance.tag_list:
                attribute_name = get_field_name_from_tag(tag['name'])
                print "tag field name ", attribute_name
                attribute_value = getattr(instance, attribute_name, '')
                attribute_list.append({'name':attribute_name,'value':attribute_value})
            print "attribute list ", attribute_list
            extra_context['attribute_list'] = attribute_list
        return extra_context
            

    def get_context(self, context,instance, attribute):
        extra_context = self._get_data_context(context, instance, attribute)
        return extra_context

register.tag(ContentRender)