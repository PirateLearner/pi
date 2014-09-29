import datetime
import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class Bookmark(models.Model):
    
    url = models.URLField(unique=True)
        
    adder = models.ForeignKey(User, related_name="added_bookmarks", verbose_name=_("adder"))
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        ordering = ["-added", ]
    

class BookmarkFolderInstance(models.Model):
    
    adder = models.ForeignKey(User, related_name="bookmarks_folder", verbose_name=_("user"))
    created = models.DateTimeField(_("created"), default=datetime.datetime.now)
    
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    

class BookmarkInstance(models.Model):
    
    bookmark = models.ForeignKey(Bookmark, related_name="saved_instances", verbose_name=_("bookmark"))
    user = models.ForeignKey(User, related_name="saved_bookmarks", verbose_name=_("user"))
    saved = models.DateTimeField(_("saved"), default=datetime.datetime.now)
    
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    image_url = models.URLField()
    folder = models.ForeignKey(BookmarkFolderInstance, verbose_name=_("folder"))
    

    def save(self, force_insert=False, force_update=False):
        if getattr(self, 'url', None):
            try:
                bookmark = Bookmark.objects.get(url=self.url)
            except Bookmark.DoesNotExist:
                # has_favicon=False is temporary as the view for adding bookmarks will change it
                bookmark = Bookmark(url=self.url, description=self.description, title=self.title, adder=self.user)
                bookmark.save()
            self.bookmark = bookmark
        super(BookmarkInstance, self).save(force_insert, force_update)
    
    def delete(self):
        bookmark = self.bookmark
        super(BookmarkInstance, self).delete()
        if bookmark.saved_instances.all().count() == 0:
            bookmark.delete()
    
    def __unicode__(self):
        return _("%(bookmark)s for %(user)s") % {"bookmark":self.bookmark, "user":self.user}