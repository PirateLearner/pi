import datetime
import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from django.db.models import Q

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from bookmarks import settings
from django.conf import settings as global_settings

if 'cms' in global_settings.INSTALLED_APPS:
    from cms.models.pluginmodel import CMSPlugin
import traceback
import sys
from django.template.defaultfilters import slugify

from PirateLearner.models import BaseContentClass

PRIVACY = (
    ('pub','public'),
    ('priv','private'),
)


class Bookmark(BaseContentClass):
    
    url = models.URLField(unique=True)
        
    adder = models.ForeignKey(User, related_name="added_bookmarks", verbose_name=_("adder"),on_delete = models.CASCADE)
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        ordering = ["-added", ]
    

class BookmarkFolderInstance(BaseContentClass):
    
    adder = models.ForeignKey(User, related_name="bookmarks_folder", verbose_name=_("user"),on_delete = models.CASCADE)
    created = models.DateTimeField(_("created"), default=datetime.datetime.now)
    
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    def __unicode__(self):
        return _("%(title)s") % {"title":self.title}

class BookmarkInstance(BaseContentClass):
    
    bookmark = models.ForeignKey(Bookmark, related_name="saved_instances", verbose_name=_("bookmark"),on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="saved_bookmarks", verbose_name=_("user"),on_delete = models.CASCADE)
    saved = models.DateTimeField(_("saved"), default=datetime.datetime.now)
    
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    note = models.TextField(_("note"), blank=True)
    image_url = models.URLField(blank=True, null=True)
    folder = models.ForeignKey(BookmarkFolderInstance, verbose_name=_("folder"),on_delete = models.CASCADE)
    privacy_level = models.CharField(choices=PRIVACY,max_length=4)
    tags = TaggableManager(blank=True)
    is_promoted = models.BooleanField(default=False);
    def save(self, url,force_insert=False, force_update=False):
        try:
            bookmark = Bookmark.objects.get(url=url)
        except Bookmark.DoesNotExist:
            # has_favicon=False is temporary as the view for adding bookmarks will change it
            bookmark = Bookmark(url=url, adder=self.user)
            bookmark.save()
        if self.folder:
            folder_name = self.folder.title
        else:
            print "Logs:folder not provided"
            folder_name = 'Orphan'
            try:
                folder = BookmarkFolderInstance.objects.get(adder = self.user,title=folder_name )
            except BookmarkFolderInstance.DoesNotExist:
                print "Logs:Creating Orphan folder for user"
                folder = BookmarkFolderInstance.create(adder = self.user,title=folder_name,description= self.description )
                folder.save()
                self.folder = folder
        if not self.privacy_level:
            self.privacy_level = 'priv'
            print "Logs: Privacy level not provided setting default to private"

        if not self.is_promoted:
            if self.user.is_staff and self.privacy_level == 'pub':
                self.is_promoted = True
            else:
                self.is_promoted = False
             
        self.bookmark = bookmark
        super(BookmarkInstance, self).save(force_insert, force_update)
    
    def delete(self):
        bookmark = self.bookmark
        super(BookmarkInstance, self).delete()
        if bookmark.saved_instances.all().count() == 0:
            bookmark.delete()
    
    def __unicode__(self):
        return _("%(bookmark)s for %(user)s") % {"bookmark":self.bookmark, "user":self.user}
    
    def get_absolute_url(self):
        kwargs = {'slug': slugify(self.title)+'/'+str(self.id),}
        return reverse('bookmarks:detail-view', kwargs=kwargs)
    
    def get_external_url(self):
        return self.bookmark.url
    
    
    def get_image_url(self):
        if len(self.image_url)>0:
            return self.image_url
        else:
            return(settings.BOOKMARK_DEFAULT_IMAGE)
    
    def get_title(self):
        return self.title

    def get_note(self):
        return self.note


    def get_summary(self):
        return self.description
    
    def get_description(self):
        return self.description
    
    def get_parent_title(self):
        return self.folder.title
    
    def get_tags(self):
        tags = self.tags.all()
        tag_list = []
        for tag in tags:
            try:
                tmp = {}
                tmp['name'] = tag.slug
                kwargs = {'tag': tag.slug,}
                tmp['url'] = reverse('bookmarks:tagged-bookmarks',kwargs=kwargs)
                tag_list.append(tmp)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print "Error in %s on line %d" % (fname, lineno)
        return tag_list

if 'cms' in global_settings.INSTALLED_APPS:
    class LatestBookmarksPlugin(CMSPlugin):
    
        latest_entries = models.IntegerField(default=5, help_text=('The number of latests entries to be displayed.'))
        tags = models.ManyToManyField('taggit.Tag', blank=True, help_text=('Show only the bookmarks tagged with chosen tags.'))
    
        def __unicode__(self):
            return str(self.latest_entries)
    
        def copy_relations(self, oldinstance):
            self.tags = oldinstance.tags.all()
    
        def get_bookmarks(self):
            posts = BookmarkInstance.objects.all().filter(user__is_staff=True,privacy_level='pub').order_by('-saved')
    #         print 'Printing get_bookmarks'
    #         for post in posts:
    #             print post
            
            tags = list(self.tags.all())
            if tags:
                posts = posts.filter(tags__in=tags)
            return posts[:self.latest_entries]


def get_bookmarks_count(user=None):
    try:
        if user:
            return BookmarkInstance.objects.filter(user = user).count()
        else:
            return BookmarkInstance.objects.count()
    except:
        return None
    
    
def get_user_bookmark(user,privacy = None):
    try:
        bookmark_instance = None
        if privacy:
            bookmark_instance = BookmarkInstance.objects.filter(user_id = user,privacy_level = privacy)
        else:
            bookmark_instance = BookmarkInstance.objects.filter(user_id = user)
        if bookmark_instance:
            return bookmark_instance
        else:
            return None
    except:
        return None
    
def get_bookmark(url):
    try:
        bookmark_instance = BookmarkInstance.objects.filter(bookmark___url = url)[0]
        if bookmark_instance:
            return bookmark_instance 
        else:
            return None
    except:
        return None
