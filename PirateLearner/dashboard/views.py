# Create your views here.
from django.shortcuts import render_to_response,RequestContext



def dashboard_home(request):
    return render_to_response('home.html',context_instance=RequestContext(request))