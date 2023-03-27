from spotlight.models import Spotlight
from django import template
register = template.Library()

@register.simple_tag
def get_feature_articles(num_entries):
    return Spotlight.objects.all().order_by('-added')[:num_entries]
