import datetime
from collections import Counter
from django.utils import timezone

from django.db import models
from django.db.models import Q

from django.contrib import auth
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager
from taggit.models import TaggedItem, Tag
from cms.models.pluginmodel import CMSPlugin


# Create your models here.

class RelatedManager(models.Manager):

    def get_query_set(self):
        qs = super(RelatedManager, self).get_query_set()
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
        tags = Tag.objects.filter(pk__in=counted_tags.keys())
        for tag in tags:
            tag.count = counted_tags[tag.pk]
        return sorted(tags, key=lambda x: -x.count)

class PublishedManager(RelatedManager):
	def get_query_set(self):
		qs = super(PublishedManager, self).get_query_set()
		now = timezone.now()
		qs = qs.filter(publication_start__lte=now)
		qs = qs.filter(Q(published_flag=True))
		return qs


class BlogContentType(models.Model):
	content_type = models.CharField(max_length = 100)
    	
	def __unicode__(self):
        	return self.content_type

class BlogParent(MPTTModel):
	name = models.CharField(max_length = 50, unique=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
	slug = models.SlugField()
    	def __unicode__(self):
        	return self.name

	def save(self, *args, **kwargs):
        	self.slug = slugify(self.name)
		super(BlogParent, self).save(*args, **kwargs)

	def form_url(self):
		parent_list = self.get_ancestors(include_self=True)
		return_path = '/'.join(word.slug for word in parent_list)
		print return_path
		return return_path

    	def get_absolute_url(self):
		kwargs = {'slug': str(self.form_url())}

    		from django.core.urlresolvers import reverse
	    	return reverse('blogging:teaser-view', kwargs=kwargs)
	
	class MPTTMeta:
            order_insertion_by = ['name']


class BlogContent(models.Model):
    title = models.CharField(max_length = 100)
    create_date = models.DateTimeField('date created', auto_now_add=True)
    author_id  = models.ForeignKey(auth.models.User)
    data = HTMLField()
    published_flag = models.BooleanField('is published?',default = 0)
    special_flag = models.BooleanField(default = 0)
    last_modified = models.DateTimeField('date modified',auto_now=True)
    url_path = models.CharField(max_length= 255)
    section = models.ForeignKey(BlogParent, limit_choices_to={'children': None})
    content_type = models.ForeignKey(BlogContentType,null=True)
    slug = models.SlugField(max_length= 100)
    tags = TaggableManager(blank=True)
    publication_start = models.DateTimeField(('Published Since'), default=timezone.now, help_text=('Used for automatic delayed publication. For this feature to work published_flag must be on.'))
    objects = RelatedManager()    
    published = PublishedManager()

    def get_absolute_url(self):
	kwargs = {'slug': self.url_path,}

        from django.core.urlresolvers import reverse
        return reverse('blogging:teaser-view', kwargs=kwargs)


    def find_path(self,section): 
	parent_list = section.get_ancestors(include_self=True)
	return_path = '/'.join(word.slug for word in parent_list)
	return_path = return_path + str("/") + self.slug + str("/") + str(self.id)
	print return_path
	return return_path


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogContent, self).save(*args, **kwargs)
        self.url_path = self.find_path(self.section)
        super(BlogContent, self).save(*args, **kwargs)
        print "after save "  + self.url_path

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_start']


class LatestEntriesPlugin(CMSPlugin):

    latest_entries = models.IntegerField(default=5, help_text=('The number of latests entries to be displayed.'))
    parent_section = models.ForeignKey(BlogParent,null=True,blank=True, limit_choices_to={'children': None})
    tags = models.ManyToManyField('taggit.Tag', blank=True, help_text=('Show only the blog posts tagged with chosen tags.'))

    def __unicode__(self):
        return str(self.latest_entries)

    def copy_relations(self, oldinstance):
        self.tags = oldinstance.tags.all()

    def get_posts(self):
	if self.parent_section:
        	posts = BlogContent.published.filter(section=self.parent_section)
	else:
		posts = BlogContent.published.all()
        tags = list(self.tags.all())
        if tags:
            posts = posts.filter(tags__in=tags)
        return posts[:self.latest_entries]

