import datetime
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from cms.models.pluginmodel import CMSPlugin
import traceback
import sys

TYPE = (
    (0,'Promoted'),
    (1,'Sponsored'),
)


class Spotlight(models.Model):
    
    type = models.IntegerField(choices=TYPE,default = 0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')        
    adder = models.ForeignKey(User, related_name="added_spotlights", verbose_name=_("adder"))
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.content_object.__str__()
    
    class Meta:
        ordering = ["-added", ]
        
class LatestSpotlightPlugin(CMSPlugin):

    latest_entries = models.IntegerField(default=1, help_text=('The number of latests featured entries to be displayed.'))
    tags = models.ManyToManyField('taggit.Tag', blank=True, help_text=('Show only the entries tagged with chosen tags.'))

    def __unicode__(self):
        return str(self.latest_entries)

    def copy_relations(self, oldinstance):
        self.tags = oldinstance.tags.all()

    def get_spotlights(self):
        posts = Spotlight.objects.all().order_by('-added')
        print "LOGS: get_spotlights called --> "
        tags = list(self.tags.all())
        if tags:
            temp = []
            for post in posts:
                if bool(sum(map(lambda x: x in tags, post.content_object.tags.all()))):
                    temp.append(post)
            posts= temp
        print posts
        return posts[:self.latest_entries]

