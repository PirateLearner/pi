from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from django.core.management import call_command
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from bookmarks.models import BookmarkInstance
from bookmarks.readability import Readability

class Command(BaseCommand):

    help = 'Update all the Bookmark instances wrt Description fields'
    
    
    def handle(self, *args, **options):
        """
        Handle command arguments
        """
        bookmark_instances = BookmarkInstance.objects.all()
        parsed_dict = {}
        for ele in bookmark_instances:
            print(('****Updating bookmark instance id ', ele.id, ' *********'));
            parsed_dict = Readability(ele.get_external_url()).parse()
            if parsed_dict['content'] is not None:
                ele.description = parsed_dict['content']
                ele.save(ele.get_external_url())
            else:
                print('****Failed try once again *********');
                parsed_dict = Readability(ele.get_external_url()).parse()
                if parsed_dict['content'] is not None:
                    ele.description = parsed_dict['content']
                    ele.save(ele.get_external_url())
                else:
                    print('****Failed again moving on *********');
            
                