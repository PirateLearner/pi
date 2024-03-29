from django.utils import timezone

import sys
from django.db import models
from django.db.models import Q

from django.contrib import auth
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItem, Tag

from django.contrib.contenttypes.fields import GenericRelation
from annotations.models import Annotation

from django.conf import settings
from django.db.models import Count, Sum

if 'cms' in settings.INSTALLED_APPS:
    try:
        from cms.models.pluginmodel import CMSPlugin
        from djangocms_text_ckeditor.models import Text
    except ImportError:
        print ('CMS not installed')

from blogging.utils import get_imageurl_from_data, truncatewords, slugify_name
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from django.urls import reverse

import reversion

import traceback
import json

from PirateLearner.models import BaseContentClass

#from south.v2 import DataMigration

# Create your models here.

LATEST_PLUGIN_TEMPLATES = (
  ('blogging/plugin/plugin_teaser.html', 'Teaser View'),
  ('blogging/plugin/plugin_section.html', 'Section View'),
  ('blogging/plugin/sidebar_list.html', 'Text List'),
  ('blogging/plugin/teaser_list.html', 'Stacked List'),
)


class RelatedManager(models.Manager):

    def get_queryset(self):
        qs = super(RelatedManager, self).get_queryset()
        return qs

    def get_tags(self, language):
        """Returns tags used to tag post and its count. Results are ordered by count."""

        # get tagged post
        entries = self.get_query_set().distinct()
        if not entries:
            return []
        kwargs = TaggedItem.bulk_lookup_kwargs(entries)

        # aggregate and sort
        counted_tags = dict(TaggedItem.objects
                                      .filter(**kwargs)
                                      .values('tag')
                                      .annotate(count=models.Count('tag'))
                                      .values_list('tag', 'count'))

        # and finally get the results
        tags = Tag.objects.filter(pk__in=list(counted_tags.keys()))
        for tag in tags:
            tag.count = counted_tags[tag.pk]
        return sorted(tags, key=lambda x: -x.count)

class PublishedManager(RelatedManager):
    def get_queryset(self):
        qs = super(PublishedManager, self).get_queryset()
        now = timezone.now()
        qs = qs.filter(publication_start__lte=now)
        qs = qs.filter(Q(published_flag=True)).order_by('-publication_start')
        return qs


class BlogContentType(BaseContentClass):
    content_type = models.CharField(max_length = 100,unique = True)
    is_leaf = models.BooleanField('Is leaf node?', default = 0)

    def __unicode__(self):
        return self.content_type

    def __str__(self):
        return str(self.content_type) or ''

    def save(self, *args, **kwargs):
        self.content_type = slugify_name(self.content_type)
        print(self.content_type)
        super(BlogContentType, self).save(*args, **kwargs)

class BlogParent(MPTTModel):
    title = models.CharField(max_length = 50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete = models.SET_NULL)
    data = models.TextField(null= False)
    content_type = models.ForeignKey(BlogContentType,null=True,default=None,on_delete = models.SET_NULL)
    slug = models.SlugField()
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        blogs = BlogContent.objects.filter(section=self.parent)
        if blogs:
            try:
                orphan_parent = BlogParent.objects.get(title='Orphan')
                for blog in blogs:
                    blog.section = orphan_parent
                    blog.save()
            except:
                print ('FATAL ERROR CAN DO NOTHING')
        super(BlogParent, self).save(*args, **kwargs)

    def form_url(self):
        parent_list = self.get_ancestors(include_self=True)
        return_path = '/'.join(word.slug for word in parent_list)
        #print( "inside absolute URL ", return_path)
        return return_path

    def get_image_url(self):
        try:
            json_obj = json.loads(self.data)
            for value in json_obj.values():
                image =  get_imageurl_from_data(value)
                if image:
                    return image
        except:
            return get_imageurl_from_data(self.data)
        return ""

    def get_absolute_url(self):
        kwargs = {'slug': str(self.form_url())}
        return reverse('blogging:teaser-view', kwargs=kwargs)
    def get_menu_title(self):
        return self.title

    def get_child_count(self):
        return self.children.count()

    def get_article_count(self):
        return BlogContent.published.filter(section = self).count()


    def get_title(self):
        return self.title

    class MPTTMeta:
            order_insertion_by = ['title']


class BlogContent(BaseContentClass):
    title = models.CharField(max_length = 100)
    create_date = models.DateTimeField('date created', auto_now_add=True)
    author_id  = models.ForeignKey(auth.models.User, related_name="blogcontent",on_delete = models.CASCADE)
    data = models.TextField(null= False)
    published_flag = models.BooleanField('is published?',default = 0)
    special_flag = models.BooleanField(default = 0)
    last_modified = models.DateTimeField('date modified',auto_now=True)
    url_path = models.CharField(max_length= 255)
    section = models.ForeignKey(BlogParent, limit_choices_to={'children': None},on_delete = models.CASCADE)
    content_type = models.ForeignKey(BlogContentType,null=True,on_delete = models.SET_NULL)
    slug = models.SlugField(max_length= 100)
    tags = TaggableManager(blank=True)
    publication_start = models.DateTimeField(('Published Since'), default=timezone.now, help_text=('Used for automatic delayed publication. For this feature to work published_flag must be on.'))
    objects = RelatedManager()
    published = PublishedManager()

    annotation = GenericRelation(Annotation, content_type_field='content_type', object_id_field='object_id')

    def get_absolute_url(self):
        kwargs = {'slug': self.url_path,}
        print ("LOGS:: Fetching URI for node")
        return reverse('blogging:teaser-view', kwargs=kwargs)

    def get_image_url(self):
        try:
            json_obj = json.loads(self.data)
            for value in json_obj.values():
                image =  get_imageurl_from_data(value)
                if image:
                    return image
            return self.section.get_image_url()
        except:
            image =  get_imageurl_from_data(self.data)
            if image:
                return image
            return self.section.get_image_url()
    def get_summary(self):
        json_obj = json.loads(self.data)
        # Instantiate the Meta class
        description = strip_tags(list(json_obj.values())[0])
        return mark_safe(truncatewords(description,120))


    def get_title(self):
        return self.title


    def find_path(self,section):
        parent_list = section.get_ancestors(include_self=True)
        return_path = '/'.join(word.slug for word in parent_list)
        return_path = return_path + str("/") + self.slug + str("/") + str(self.id)
        print (return_path)
        return return_path

    def get_menu_title(self):
        return self.title

    def get_parent(self):
        return self.section

    def get_tags(self):
        tags = self.tags.all()
        tag_list = []
        for tag in tags:
            try:
                tmp = {}
                tmp['name'] = tag.name
                kwargs = {'tag': tag.slug,}
                tmp['url'] = reverse('blogging:tagged-posts',kwargs=kwargs)
                tag_list.append(tmp)
            except:
                print(("Unexpected error:", sys.exc_info()[0]))
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print(("Error in %s on line %d" % (fname, lineno)))
        return tag_list

    def get_author(self):
        print((self.author_id)) #Anshul: Changed, don't remember why. Maybe in REST
        return self.author_id
        #return self.author_id.first_name or self.author_id.username
    def get_modified_year(self):
        print(("LAst Modified year is ", self.last_modified.year))
        return self.last_modified.year

    def get_modified_month(self):
        return self.last_modified.month
    def get_modified_day(self):
        return self.last_modified.day

    def get_modified_time(self):
        current_year = timezone.now().year
        current_day = timezone.now().day
        print(("Printing localtime ", timezone.localtime(self.last_modified)))
        desired_time = timezone.localtime(self.last_modified)

        if(self.last_modified.year < current_year):
            return self.last_modified.strftime("%d/%m/%Y")
        elif(current_day == self.last_modified.day):
            return desired_time.strftime("%I:%M %P")
            #return self.last_modified
        else:
            return self.last_modified.strftime("%B, %d")

    def get_published_year(self):
        pass
    def get_published_month(self):
        pass
    def get_published_day(self):
        pass
    
    def get_body_content(self):
        return self.body.decode("utf-8");

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogContent, self).save(*args, **kwargs)
        self.url_path = self.find_path(self.section)
        super(BlogContent, self).save(*args, **kwargs)

    def __str__(self):
        return self.title or ''

    class Meta:
        ordering = ['-publication_start']

if 'cms' in settings.INSTALLED_APPS:
    class LatestEntriesPlugin(CMSPlugin):

        latest_entries = models.IntegerField(default=5, help_text=('The number of latests entries to be displayed.'))
        parent_section = models.ForeignKey(BlogParent,null=True,blank=True)
        tags = models.ManyToManyField('taggit.Tag', blank=True, help_text=('Show only the blog posts tagged with chosen tags.'))
        template = models.CharField('Template', max_length=255,
                                    choices = LATEST_PLUGIN_TEMPLATES, default='blogging/plugin/plugin_teaser.html')
        def __unicode__(self):
            return str(self.latest_entries)

        def copy_relations(self, oldinstance):
            self.tags = oldinstance.tags.all()

        def get_posts(self):
            if self.parent_section:
                if self.parent_section.is_leaf_node():
                    posts = BlogContent.published.filter(section=self.parent_section)
                else:
                    parent_list = self.parent_section.get_descendants()
                    posts = BlogContent.published.filter(section__in=parent_list)
            else:
                posts = BlogContent.published.all()

            tags = list(self.tags.all())
            if tags:
                posts = posts.filter(tags__in=tags)
            return posts[:self.latest_entries]

        def get_section(self):
            return self.parent_section



    class SectionPlugin(CMSPlugin):

        section_count = models.IntegerField(default=None, blank=True,null=True, help_text=('The number of sections to be displayed.'))
        parent_section = models.ForeignKey(BlogParent,null=True,blank=True)

        def __unicode__(self):
            return str(self.section_count)

        def get_sections(self):
            if self.parent_section:
                sections = self.parent_section.get_children()
            else:
                sections = BlogParent.objects.all(~Q(title='Orphan'),level=0)
            if self.section_count:
                return sections[:self.section_count]
            return sections

    class ContactPlugin(CMSPlugin):
        to_email = models.EmailField(default= 'captain@piratelearner.com')
        thanks_text = models.CharField(max_length=100,default = 'Thanks for reaching out to Us. We will get back to you soon.')
        def __unicode__(self):
            return 'ContactPlugin'
        def thanks(self):
            return self.thanks_text


def get_published_count(user = None):
    if user:
        return BlogContent.objects.filter(published_flag=True,author_id=user).count()
    else:
        return BlogContent.objects.filter(published_flag=True).count()

def get_pending_count(user = None):
    if user:
        return BlogContent.objects.filter(published_flag=False,special_flag=False,author_id=user).count()
    else:
        return BlogContent.objects.filter(published_flag=False,special_flag=False).count()

def get_draft_count(user = None):
    if user:
        return BlogContent.objects.filter(published_flag=False,special_flag=True,author_id=user).count()
    else:
        return BlogContent.objects.filter(published_flag=False,special_flag=True).count()

def get_contribution_count(user):
    if user:
        return BlogContent.objects.filter(author_id=user).count()
    else:
        return None
def get_top_articles(user = None, limit = 5):
    if user:
#         return BlogContent.objects.filter(author_id=user).annotate(score=Sum('vote')).order_by('score')
        return BlogContent.published.filter(author_id=user)
    else:
        return Vote.objects.get_top(BlogContent)

# class VersionMeta(models.Model):
#     revision = models.ForeignKey(Revision)  # There must be a relationship with Revision
#     published_flag = models.BooleanField('is published?',default = 0)

"""
class Migration(DataMigration):
	def forwards(self, orm):
        	"Write your forwards methods here."
        	BlogParent.objects.rebuild()
"""

if not reversion.is_registered(BlogContent):
    reversion.register(BlogContent,fields=["title","data"])
if not reversion.is_registered(BlogParent):
    reversion.register(BlogParent,fields=["title","data"])
