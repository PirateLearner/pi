class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)
        
    def get_plugins(self,cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins]

    def get_plugin_list(self,cls, *args, **kwargs):
        return cls.plugins


class ActionProvider(metaclass=PluginMount):
    """
    Mount point for plugins which refer to actions that can be performed.

    Plugins implementing this reference should provide the following attributes:

    ========  ========================================================
    title     The text to be displayed, describing the action

    width     width of the rendred area in terms of pixel or columns

    height    Minimum height of the plugin in pixels

    render_plugin    function that should return the HttpResponse
    ========  ========================================================
    """
    
    
    
class PluginTest1(ActionProvider):
    title = "Test Plugin 1"
    width = 50
    height = 50

class PluginTest2(ActionProvider):
    title = "Test Plugin 2"
    width = 40
    height = 60

class PluginTest3(ActionProvider):
    title = "Test Plugin 3"
    width = 60
    height = 30
    
    