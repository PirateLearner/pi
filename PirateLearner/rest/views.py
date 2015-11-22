from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status

from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView

from rest.serializers import *
from rest.utils import IsOwnerOrReadOnly, AnnotationIsOwnerOrReadOnly, VoteIsOwnerOrReadOnly, BookmarkIsOwnerOrReadOnly


@api_view(('GET',))
#If not set, the API root will assert for not having appropriate permissions.
@permission_classes((permissions.IsAuthenticatedOrReadOnly, ))
def api_root(request, format=None):
    return Response({
        'blogcontent': reverse('rest:blogcontent-list', request=request, format=format),
        'user': reverse('rest:user-list', request=request, format=format),
        'annotations': reverse('rest:annotations-list', request=request, format=format),
        'currentUser': reverse('rest:current-user', request=request, format=format),
        'vote': reverse('rest:vote-list', request=request, format=format),
        'bookmarks': reverse('rest:bookmarks-list', request=request, format=format),            
        })
 
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        user_obj = self.request.user
        if(user_obj.id != None):
            serializer = UserSerializer(user_obj)
        else:
            serializer = AnonymousUserSerializer(user_obj)
            #print(serializer.data)
             
        return Response(serializer.data)    
        
class BlogContentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)



class VoteViewSet(viewsets.ModelViewSet):
    
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          VoteIsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(voter=self.request.user)

class VoteList(APIView):
    """
    List all votes, or create a new vote.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,VoteIsOwnerOrReadOnly,)
    
    def get(self, request, format=None):
        print 'in get'
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'in post'
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            content_type = serializer.validated_data.get('content_type')
            object_id = serializer.validated_data.get('object_id')
        
            #Get row from contentType which has content_type
            ct_object = ContentType.objects.get_for_id(content_type.id)
            
            content_object = ct_object.model_class().objects.get(id=object_id)
            
            author = content_object.get_author()
            if  author == request.user:
                serializer.errors['detail'] = 'Author of post is not allowed to vote on it'
                return Response({'detail' : "Author of post is not allowed to vote on it"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(voter=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,VoteIsOwnerOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(voter=self.request.user)


class BlogContentVoteView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        #First, get the model instance of BlogContent
        obj = BlogContent.objects.get(pk=pk)
        #Then, get the content type instance
        content_type = ContentType.objects.get_for_model(obj)
        vote = Vote.objects.filter(content_type= content_type.id, object_id=obj.id)
        
        #print vote
        
        #Now, put them into a serializer
        serializer = VoteSerializer(vote, many=True)
        return Response(serializer.data)
        

class AnnotationViewSet(viewsets.ModelViewSet):
    
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          AnnotationIsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogContentCommentView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, pk, format=None):
        #First, get the model instance of BlogContent
        obj = BlogContent.objects.get(pk=pk)
        #Then, get the content type instance
        content_type = ContentType.objects.get_for_model(obj)
        annotations = Annotation.objects.filter(content_type= content_type.id, object_id=obj.id)
        print annotations
        
        #Now, put them into a serializer
        serializer = AnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
    
class BookmarkList(generics.ListCreateAPIView):
    queryset = BookmarkInstance.objects.all()
    serializer_class = BookmarkInstanceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          BookmarkIsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookmarkInstance.objects.all()
    serializer_class = BookmarkInstanceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    