from rest_framework import serializers
from models import Annotation

from blogging.models import BlogContent, BlogParent
from django.contrib.auth.models import User

from generic_relations.relations import GenericRelatedField

class BlogParentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogParent
        fields = ('title', 'parent', 'data')
     

class BlogContentSerializer(serializers.ModelSerializer):
    #annotation = serializers.RelatedField()
    author_id = serializers.Field(source='author_id.username')
    annotation = serializers.RelatedField(many=True)
    
    class Meta:
        model = BlogContent
        fields = ('title','create_date','author_id',
                  'data','published_flag','special_flag',
                  'last_modified','url_path', 
                  'slug','annotation',)
        #exclude = ('section','content_type',)
        

class AnnotationSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user.username')
    content_object = GenericRelatedField({
        BlogContent: serializers.HyperlinkedRelatedField(view_name='rest:annotation:blogcontent-detail'),
        #BlogContent: BlogContentSerializer(),
    }, read_only=False)
    
    class Meta:
        model = Annotation
        fields = ('id','paragraph_id', 'body', 'user', 'privacy', 'privacy_override_flag', 'shared_with', 'submit_date', 'last_modify_date','content_object', 'site')


class UserSerializer(serializers.ModelSerializer):
    blogcontent= serializers.PrimaryKeyRelatedField(many=True) 
    annotations = serializers.PrimaryKeyRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ('username', 'id', 'blogcontent', 'annotations')  
        
class AnonymousUserSerializer(serializers.Serializer):
    username = serializers.CharField();
    
 