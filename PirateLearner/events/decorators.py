from threading import Thread
from . import signals
from events.models import EventType, InvalidEvent
from django.core.exceptions import ObjectDoesNotExist

from exceptions import ValueError

_registry = {}


def  register_handle(label):
    def decorate(func):
        
        try:
            event_label = str(label)
        except:
            raise ValueError("label need to be str object")
        try:
            event = EventType.objects.get(label=event_label)
        except ObjectDoesNotExist:
            raise InvalidEvent(event_label)
        _registry.setdefault(event_label, []).append(func)
        return func
    return decorate

## connect to the signal defined in signals.py

def execute_actions(*args, **kwargs):
    '''
    This function will executes the functions registered for particular label. For now it will create new thread for each functions.
    @warning: It can hawk the system if more numbers of threads have been created.
    '''


    if kwargs:
        label = kwargs.get('event_label',None)

    if label is None:
        label = args[1]


    for func in _registry.get(label,None):
        t = Thread(target = func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        
        

signals.generate_event.connect(execute_actions, weak=False,dispatch_uid="action_identifier")