

import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured

from events.compat import get_model

from appconf import AppConf


def load_model(path):
    try:
        return get_model(path)
    except ValueError:
        raise ImproperlyConfigured(
            "{0} must be of the form 'app_label.model_name'".format(path)
        )
    except LookupError:
        raise ImproperlyConfigured("{0} has not been installed".format(path))


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


def is_installed(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False


class EventsNotificationsAppConf(AppConf):

    LINK_PROTOCOL = "http"
    BACKENDS = [
        ("email", "events.backends.email.EmailBackend"),
    ]

    def configure_backends(self, value):
        backends = []
        for medium_id, bits in enumerate(value):
            if len(bits) == 2:
                label, backend_path = bits
                spam_sensitivity = None
            elif len(bits) == 3:
                label, backend_path, spam_sensitivity = bits
            else:
                raise ImproperlyConfigured(
                    "NOTIFICATION_BACKENDS does not contain enough data."
                )
            backend_instance = load_path_attr(backend_path)(medium_id, spam_sensitivity)
            backends.append(((medium_id, label), backend_instance))
        return dict(backends)

    class Meta:
        prefix = "events_notifications"
