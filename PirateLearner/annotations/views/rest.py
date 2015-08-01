from annotations.models import Annotation
from blogging.models import BlogContent, BlogParent
from django.contrib.auth.models import User

from rest_framework import viewsets

from annotations.serializers import *

from rest_framework import permissions
from utils import IsOwnerOrReadOnly, AnnotationIsOwnerOrReadOnly

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BlogParentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogParent.objects.all()
    serializer_class = BlogParentSerializer
    
    
class BlogContentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

class AnnotationViewSet(viewsets.ModelViewSet):
    
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, AnnotationIsOwnerOrReadOnly,)
            
# From hence, all models are representation of things that don't actually exist

from django.contrib.contenttypes.models import ContentType 
from rest_framework.views import APIView

class BlogContentCommentView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        #First, get the model instance of BlogContent
        obj = BlogContent.objects.get(pk=pk)
        #Then, get the content type instance
        content_type = ContentType.objects.get_for_model(obj)
        annotations = Annotation.objects.filter(content_type= content_type.id, object_pk=obj.id)
        print annotations
        
        #Now, put them into a serializer
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
        

class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        user_obj = self.request.user
        if(user_obj.id != None):
            serializer = UserSerializer(user_obj)
        else:
            serializer = AnonymousUserSerializer(user_obj)
            print(serializer.data)
             
        return Response(serializer.data)

