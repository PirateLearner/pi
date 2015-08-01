from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User

from bookmarks.models import Bookmark, PRIVACY, BookmarkFolderInstance, BookmarkInstance


class BookmarkInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkInstance
        fields = ('id', 'title', 'description', 'image_url', 'folder', 'privacy_level')
    
class BookmarkSerializer(serializers.ModelSerializer):
    adder = serializers.Field(source='adder.username')
    bookmark = serializers.RelatedField(many=True)
    class Meta:
        model = Bookmark
        fields = ('id', 'url', 'adder','bookmark')

class BookmarkFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkFolderInstance
        fields = ('id', 'title', 'description', 'image_url', 'folder', 'privacy_level')

class BookMarksUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'id', 'blogcontent', 'annotations')  
        
class AnonymousBookmarksUserSerializer(serializers.Serializer):
    username = serializers.CharField();