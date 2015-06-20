from django.contrib.auth.models import User
from rest_framework import viewsets

from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse# Create your views here.



@api_view(('GET',))
#If not set, the API root will assert for not having appropriate permissions.
@permission_classes((permissions.IsAuthenticatedOrReadOnly, ))
def api_root(request, format=None):
    return Response({
        'blogcontent': reverse('rest:annotation:blogcontent-list', request=request, format=format),
        'user': reverse('rest:annotation:user-list', request=request, format=format),
        'annotations': reverse('rest:annotation:annotation-list', request=request, format=format),
        'currentUser': reverse('rest:annotation:current-user', request=request, format=format),            
        })
 