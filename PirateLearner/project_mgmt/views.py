# Create your views here.
import ConfigParser
from django.template import RequestContext, loader
from django.http import HttpResponse
from .utils import parse_feature
import os, errno



def index(request):

    feature_list = parse_feature()
    completed = []
    started = []
    pending = []
    for element in feature_list:
        print element['status'], element['completed']
        if element['completed'] == 'YES':
            completed.append(element)
        elif element['status'] != '0':
            started.append(element)
        else:
            pending.append(element)
              
    render_list = completed[0:2] + started[0:2] + pending[0:1] 
    
    template = loader.get_template('project_mgmt/wishlist.html')
    context = RequestContext(request, {
                                       'features': render_list,
                                      })
    return HttpResponse(template.render(context))
