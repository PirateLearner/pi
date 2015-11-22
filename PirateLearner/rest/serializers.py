'''
Created on 07-Jun-2015

@author: craft
'''
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

#Blogging App imports
from blogging.models import BlogContent

#User model imports
from django.contrib.auth.models import User

#Generic ContentType imports
from django.contrib.contenttypes.models import ContentType

#Voting App serializers
from voting.models import Vote, UPVOTE, DOWNVOTE

#bookmark app models
from bookmarks.models import Bookmark, PRIVACY, BookmarkFolderInstance, BookmarkInstance

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

ZERO_VOTES_ALLOWED = getattr(settings, 'VOTING_ZERO_VOTES_ALLOWED', False)

#Annotation App imports
from annotations.models import Annotation, AnnotationShareMap

#User Serializer Classes
class UserSerializer(serializers.ModelSerializer):
    
    annotations = serializers.PrimaryKeyRelatedField(many=True, 
                                                     queryset=Annotation.objects.all())
    gravatar = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    voted = serializers.PrimaryKeyRelatedField(many=True, queryset=Vote.objects.all())
    saved_bookmarks = serializers.PrimaryKeyRelatedField(many=True, queryset=BookmarkInstance.objects.all())
    bookmarks_folder = serializers.PrimaryKeyRelatedField(many=True, queryset=BookmarkFolderInstance.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'annotations', 'gravatar', 'url', 'voted','saved_bookmarks','bookmarks_folder',)
        
    def get_gravatar(self, obj):
        return '#'
    
    def get_url(self, obj):
        return '#'


class AnonymousUserSerializer(serializers.Serializer):
    username = serializers.CharField();

#Blogging App serializer Classes

class BlogContentSerializer(serializers.ModelSerializer):
    #Tell BlogContent that it has a relation on Annotations    
    annotations = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()
    uservote = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogContent
        fields =('id', 'title', 'create_date', 'data', 'url_path', 
                 'author_id', 'published_flag', 'section', 'content_type',
                 'annotations', 'vote', 'uservote',)
     
    def get_annotations(self, obj):
        content_object = ContentType.objects.get_for_model(obj)
        print "In BlogContentSerializer"
        print obj
        annotations =  Annotation.objects.filter(content_type=content_object.id, object_id=obj.id)
        if len(annotations) is not 0:
            print AnnotationSerializer(annotations, many=True).data
            return (AnnotationSerializer(annotations, many=True).data)
        else:
            return None
    
    def get_vote(self, obj):
        vote = Vote.objects.get_score(obj)
        if vote is not None:
            return vote        
        else:
            return None 
        
    def get_uservote(self, obj):        
        user = self.context['request'].user
        vote = Vote.objects.get_for_user(obj, user)
        #uservote = {'user': UserSerializer(user),
        #            'vote': json.dumps(Vote.objects.get_for_user(obj, user))
        #            }
        return (VoteSerializer(vote).data)
    
#Voting App serializers
class VoteSerializer(serializers.ModelSerializer):
    
    voter = UserSerializer(read_only=True)
    
    class Meta:
        model = Vote
        fields = (
                  'id', 'voter', 'vote', 'vote_modified', 'content_type', 'object_id',
                  )
    
    def create(self, validated_data):
        print 'In create'        
        vote = Vote()
        vote.voter = validated_data.get('voter')
        vote.vote = validated_data.get('vote')
        vote.content_type = validated_data.get('content_type')
        vote.object_id = validated_data.get('object_id')
        
        #Get row from contentType which has content_type
        content_object = ContentType.objects.get_for_id(vote.content_type.id)
        
        vote.content_object = content_object.model_class().objects.get(id=vote.object_id)
                        
        """
        Record a user's vote on a given object. Only allows a given user
        to vote once, though that vote may be changed.
        
        A zero vote indicates that any existing vote should be removed.
        """
        if vote.vote not in (+1, 0, -1):
            raise ValueError('Invalid vote (must be +1/0/-1)')
        
        # First, try to fetch the instance of this row from DB
        # If that does not exist, then it is the first time we're creating it
        # If it does, then just update the previous one
        try:
            vote_obj = Vote.objects.get(voter=vote.voter, content_type=vote.content_type, object_id=vote.object_id)
            if vote == 0 and not ZERO_VOTES_ALLOWED:
                vote_obj.delete()
            else:
                vote_obj.vote = vote
                vote_obj.save()
                
        except ObjectDoesNotExist:
            #This is the first time we're creating it
            try:
                if not ZERO_VOTES_ALLOWED and vote == 0:
                    # This shouldn't be happening actually
                    return
                vote_obj = Vote.objects.create(voter=vote.voter, content_type=vote.content_type, object_id=vote.object_id, vote=vote.vote)                        
            except:
                print '{file}: something went wrong in creating a vote object at {line}'.format(file=str('__FILE__'), line=str('__LINE__'))
                raise ObjectDoesNotExist    
        
        return vote_obj
    
    def update(self, instance, validated_data):
        vote = instance
                
        vote.voter = validated_data.get('voter', vote.voter)
        
        vote.vote += validated_data.get('vote', vote.vote)
          
        vote.content_type = validated_data.get('content_type',vote.content_type)
        vote.object_id = validated_data.get('object_id',vote.object_id)

        if vote.vote is not 0:
            vote.vote = vote.vote/abs(vote.vote)
        vote.save()
                
        return vote

#Annotations app serializers
    
class SerializeReadOnlyField(ReadOnlyField):
    
    def to_representation(self, value):
        if isinstance(value, BlogContent):
            return value.get_absolute_url()

class SerializeAnnotationsField(serializers.SerializerMethodField):
    
    def to_representation(self, value):
        print 'to_repr'
        print type(value)
        if isinstance(value, Annotation):
            return AnnotationSerializer(value)
        if isinstance(value, dict):
            print 'Is annotations'
            return AnnotationSerializer(value, many=True)

class AnnotationShareMapSerializer(serializers.ModelSerializer):    
    class Meta:
        model=AnnotationShareMap
        fields = ('user','annotations', 'notified_flag')    



class AnnotationSerializer(serializers.ModelSerializer):
    #I want the content object is a hyperlink to the ContentObject
    content_object = SerializeReadOnlyField()
    
    shared_with = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    #author = serializers.ReadOnlyField(source='author.username')
    author = UserSerializer(read_only=True)
    class Meta:
        model = Annotation
        fields = ('content_type', 'object_id', 'id',  'date_created', 'date_modified','content_object',
                  'body', 'paragraph', 
                  'author', 'shared_with',
                  'privacy', 'privacy_override', )  
    
    def create(self, validated_data):
        print "In create"
        print validated_data
        annotation = Annotation()
        annotation.author = validated_data.get('author')
        annotation.body = validated_data.get('body')
        annotation.content_type = validated_data.get('content_type')
        annotation.object_id = validated_data.get('object_id')
        annotation.paragraph = validated_data.get('paragraph')
        
        annotation.privacy = validated_data.get('privacy')
        annotation.privacy_override = validated_data.get('privacy_override', False)

        #Get row from contentType which has content_type
        content_object = ContentType.objects.get_for_id(annotation.content_type.id)
        
        annotation.content_object = content_object.model_class().objects.get(id=annotation.object_id)
        
        print annotation.content_object          
        annotation.save()

        print validated_data.get('shared_with')
        for user in validated_data.get('shared_with'):
            sharing = AnnotationShareMap(annotation=annotation, 
                                                    user=user)
            sharing.save()
        
        return annotation
    
    def update(self, instance, validated_data):
        print "In update"
        annotation = instance
        annotation.author = validated_data.get('author', annotation.author)
        annotation.body = validated_data.get('body', annotation.body)
        annotation.content_type = validated_data.get('content_type',annotation.content_type)
        annotation.object_id = validated_data.get('object_id',annotation.object_id)
        annotation.paragraph = validated_data.get('paragraph',annotation.paragraph)
        
        annotation.privacy = validated_data.get('privacy',annotation.privacy)
        annotation.privacy_override = validated_data.get('privacy_override',annotation.privacy_override)

        #Get row from contentType which has content_type
        content_object = ContentType.objects.get_for_id(annotation.content_type.id)        
        annotation.content_object = content_object.model_class().objects.get(id=annotation.object_id)        
        
        print annotation.content_object     
                
        annotation.save()
        
        print validated_data.get('shared_with')
        for user in validated_data.get('shared_with'):
            sharing = AnnotationShareMap(annotation=annotation, 
                                                    user=user)
            sharing.save()
        return annotation    
    
class BookmarkInstanceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = BookmarkInstance
        fields = ('id', 'title','user', 'description', 'image_url', 'folder', 'privacy_level')
    
    