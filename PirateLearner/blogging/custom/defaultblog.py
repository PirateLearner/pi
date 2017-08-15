from blogging import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import json
from django.db.models import Q 
from mptt.forms import TreeNodeChoiceField
from taggit.models import Tag
import blogging

"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""

class DefaultblogForm(forms.Form):
    content =  forms.CharField(widget = CKEditorUploadingWidget(config_name='author'))
    title = forms.CharField(max_length = 100)
    tags = Select2ChoiceField(queryset=Tag.objects.filter())
    section = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),Q(children=None)),required=True,empty_label=None, label = "Select Section" )
    pid_count = forms.IntegerField(required=False)
    def __init__(self,action, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        if instance:
            json_data = json.loads(instance.data)
            kwargs.update(initial={
                          # 'field': 'value'
                          'title': instance.title,
                          'section': instance.section,
                          'Body': json_data['Body'],
                          'pid_count': json_data['pid_count'],
                          'tags':  instance.tags.all()
                         })
        super(DefaultblogForm, self).__init__(*args, **kwargs)
        

    
    def save(self,post,commit=False):
        post.pop('section')
        post.pop('tags')
        post.pop('title')
        post.pop('csrfmiddlewaretoken')
        post.pop('submit')

        if commit == False:
            for k,v in post.iteritems():
                if str(k) == 'pid_count' :
                    post['pid_count'] = self.cleaned_data["pid_count"]
                else:
                    post[k] = str(v.encode('utf-8'))
            return json.dumps(post.dict())
        
        print "LOGS: Going to insert id's"
        for k,v in post.iteritems():
            if str(k) != 'pid_count' :
                tmp = {}
                tmp = tag_lib.insert_tag_id(str(v.encode('utf-8')),self.cleaned_data["pid_count"])
                post[k] = tmp['content']
                post['pid_count'] = tmp['pid_count']
            
        return json.dumps(post.dict())    


from django.db import models
class DefaultBlogModel(blogging.models.BlogContent):
    content = models.TextField()
    pid_count = models.PositiveIntegerField(blank=True)
    
    def __init__(self, *args, **kwargs):
        if 'content' in kwargs:
            body = kwargs.pop('content')
        else:
            body = None
        if 'pid_count' in kwargs:
            pid_count = kwargs.pop('pid_count')
        else:
            pid_count = None
        super(ArticleModel, self).__init__(*args, **kwargs)
        delattr(self, 'data')
        self.content = body
        self.pid_count = pid_count
        
    
    def save(self, *args, **kwargs):
        if self.id is not None:
            article = blogging.models.BlogContent.objects.get(id=self.id)
        else:        
            article = blogging.models.BlogContent()
        article.title = self.title
        article.section = self.section
        article.tags = self.tags
        article.author_id = self.author_id
        article.slug = self.slug
        
        article.content_type = BlogContentType.objects.filter(content_type=__name__.split('.')[-1])[0]
        
        post_content = {}
        
        post_content['pid_count'] = self.pid_count
        
        fields = kwargs.pop('fields')
        
        for field in fields:
            post_content[field] = getattr(self,field).encode('utf-8')
                
        article.data = json.dumps(post_content)
        article.save()
        
        return article
        
    
from rest_framework import serializers
from django.template.defaultfilters import slugify

class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=False)
    
    class Meta:
        model = DefaultBlogModel
        fields = ('id', 'content', 'title', 'section', 'tags', 'pid_count', 'author_id')
        
    def create(self, validated_data):
        article = DefaultBlogModel()
        article.id = validated_data.get('id', None) 
        article.title = validated_data.get('title')
        article.section = validated_data.get('section')
        article.tags = validated_data.get('tags')
        article.author_id = validated_data.get('author_id')
                
        article.slug = slugify(article.title)
        article.pid_count = validated_data.get('pid_count')
        article.content = validated_data.get('content')
            
        fields = [field for field in self.fields if field not in ['id', 'title', 'section', 'tags', 'pid_count', 'pid_count', 'author_id']]    
        return article.save(fields = fields)