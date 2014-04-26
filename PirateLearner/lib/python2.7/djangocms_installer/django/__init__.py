# -*- coding: utf-8 -*-
import sys
import os
import re

import shutil
import glob
import subprocess
from copy import copy

import six

from ..compat import iteritems
from ..utils import chdir
from ..config import data, get_settings


def create_project(config_data):
    """
    Call django-admin to create the project structure
    """
    from django.core.management import call_command

    kwargs = {}
    args = []
    if config_data.template:
        kwargs['template'] = config_data.template
    args.append(config_data.project_name)
    if config_data.project_directory:
        args.append(config_data.project_directory)
        if not os.path.exists(config_data.project_directory):
            os.makedirs(config_data.project_directory)

    call_command('startproject', *args, **kwargs)


def copy_files(config_data):
    """
    It's a little rude actually: it just overwrites the django-generated urls.py
    with a custom version and put other files in the project directory.
    """
    urlconf_path = os.path.join(os.path.dirname(__file__), '../config/urls.py')
    share_path = os.path.join(os.path.dirname(__file__), '../share')
    template_path = os.path.join(share_path, 'templates')
    template_target = os.path.join(config_data.project_path, 'templates')
    static_project = os.path.join(config_data.project_directory, 'static')
    static_main = os.path.join(config_data.project_path, 'static')

    if config_data.bootstrap == 'yes':
        template_path = os.path.join(template_path, 'bootstrap')
    else:
        template_path = os.path.join(template_path, 'basic')

    shutil.copy(urlconf_path, config_data.urlconf_path)
    os.makedirs(static_main)
    os.makedirs(static_project)
    os.makedirs(template_target)
    for filename in glob.glob(os.path.join(template_path, '*.html')):
        if os.path.isfile(filename):
            shutil.copy(filename, template_target)

    if config_data.starting_page:
        for filename in glob.glob(os.path.join(share_path, 'starting_page.*')):
            if os.path.isfile(filename):
                shutil.copy(filename, os.path.join(config_data.project_path, '..'))


def patch_settings(config_data):
    """
    Modify the settings file created by Django injecting the django CMS
    configuration
    """
    overridden_settings = ('MIDDLEWARE_CLASSES', 'INSTALLED_APPS',
                           'TEMPLATE_LOADERS', 'TEMPLATE_CONTEXT_PROCESSORS',
                           'TEMPLATE_DIRS', 'LANGUAGES')

    if not os.path.exists(config_data.settings_path):
        sys.stdout.write("Error while creating target project, please check the given configuration")
        return sys.exit(5)

    with open(config_data.settings_path, 'r') as fd_original:
        original = fd_original.read()

    original = original.replace("# -*- coding: utf-8 -*-\n", "")

    if original.find('BASE_DIR') == -1:
        original = data.DEFAULT_PROJECT_HEADER + data.BASE_DIR + original
    else:
        original = data.DEFAULT_PROJECT_HEADER + original
    if original.find('MEDIA_URL') > -1:
        original = original.replace("MEDIA_URL = ''", "MEDIA_URL = '/media/'")
    else:
        original += "MEDIA_URL = '/media/'\n"
    if original.find('MEDIA_ROOT') > -1:
        original = original.replace("MEDIA_ROOT = ''", "MEDIA_ROOT = os.path.join(BASE_DIR, 'media')")
    else:
        original += "MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"
    if original.find('STATIC_ROOT') > -1:
        original = original.replace("STATIC_ROOT = ''", "STATIC_ROOT = os.path.join(BASE_DIR, 'static')")
    else:
        original += "STATIC_ROOT = os.path.join(BASE_DIR, 'static')\n"
    if original.find('STATICFILES_DIRS') > -1:
        original = original.replace(data.STATICFILES_DEFAULT, """
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '%s', 'static'),
)
""" % config_data.project_name)
    else:
        original += """
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '%s', 'static'),
)
""" % config_data.project_name
    original = original.replace("# -*- coding: utf-8 -*-\n", "")

    # I18N
    if config_data.i18n == 'no':
        original = original.replace("I18N = True", "I18N = False")
        original = original.replace("L10N = True", "L10N = False")

    # TZ
    if config_data.use_timezone == 'no':
        original = original.replace("USE_TZ = True", "USE_TZ = False")

    if config_data.languages:
        original = original.replace("LANGUAGE_CODE = 'en-us'", "LANGUAGE_CODE = '%s'" % config_data.languages[0])
    if config_data.timezone:
        original = original.replace("TIME_ZONE = 'America/Chicago'", "TIME_ZONE = '%s'" % config_data.timezone)

    for item in overridden_settings:
        item_re = re.compile(r"%s = [^\)]+\)" % item, re.DOTALL | re.MULTILINE)
        original = item_re.sub('', original)
    # DATABASES is a dictionary, so different regexp needed
    item_re = re.compile(r"DATABASES = [^\}]+\}[^\}]+\}", re.DOTALL | re.MULTILINE)
    original = item_re.sub('', original)
    if original.find('SITE_ID') == -1:
        original += "SITE_ID = 1\n\n"

    original += _build_settings(config_data)

    with open(config_data.settings_path, "w") as fd_dest:
        fd_dest.write(original)


def _build_settings(config_data):
    """
    Build the django CMS settings dictionary
    """
    spacer = "    "
    text = []
    vars = get_settings()

    if config_data.django_version < 1.6:
        vars.MIDDLEWARE_CLASSES.extend(vars.MIDDLEWARE_CLASSES_DJANGO_15)

    text.append("TEMPLATE_LOADERS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.TEMPLATE_LOADERS])))

    text.append("MIDDLEWARE_CLASSES = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.MIDDLEWARE_CLASSES])))

    text.append("TEMPLATE_CONTEXT_PROCESSORS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.TEMPLATE_CONTEXT_PROCESSORS])))

    text.append("TEMPLATE_DIRS = (\n%s%s\n)" % (
        spacer, "os.path.join(BASE_DIR, '%s', 'templates')," % config_data.project_name))

    apps = list(vars.INSTALLED_APPS)
    if config_data.cms_version == 2.4:
        apps.extend(vars.CMS_2_APPLICATIONS)
    else:
        apps = list(vars.CMS_3_HEAD) + apps
        apps.extend(vars.CMS_3_APPLICATIONS)

    if config_data.cms_version == 2.4:
        if config_data.filer:
            apps.extend(vars.FILER_PLUGINS_2)
        else:
            apps.extend(vars.STANDARD_PLUGINS_2)
    else:
        if config_data.filer:
            apps.extend(vars.FILER_PLUGINS_3)
        else:
            apps.extend(vars.STANDARD_PLUGINS_3)
    if config_data.reversion:
        apps.extend(vars.REVERSION_APPLICATIONS)
    text.append("INSTALLED_APPS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in apps] + ["'%s'" % config_data.project_name])))

    text.append("LANGUAGES = (\n%s%s\n%s%s\n)" % (
        spacer, "## Customize this",
        spacer, ("\n" + spacer).join(["('%s', gettext('%s'))," % (item, item) for item in config_data.languages])))

    cms_langs = vars.CMS_LANGUAGES
    for lang in config_data.languages:
        lang_dict = {'code': lang, 'name': lang}
        lang_dict.update(copy(cms_langs['default']))
        cms_langs[1].append(lang_dict)
    cms_text = ["CMS_LANGUAGES = {"]
    cms_text.append("%s%s" % (spacer, "## Customize this",))
    for key, value in iteritems(cms_langs):
        if key == 'default':
            cms_text.append("%s'%s': {" % (spacer, key))
            for config_name, config_value in iteritems(value):
                cms_text.append("%s'%s': %s," % (spacer*2, config_name, config_value))
            cms_text.append("%s}," % spacer)
        else:
            cms_text.append("%s%s: [" % (spacer, key))
            for lang in value:
                cms_text.append("%s{" % (spacer*2))
                for config_name, config_value in iteritems(lang):
                    if config_name == 'code':
                        cms_text.append("%s'%s': '%s'," % (spacer*3, config_name, config_value))
                    elif config_name == 'name':
                        cms_text.append("%s'%s': gettext('%s')," % (spacer*3, config_name, config_value))
                    else:
                        cms_text.append("%s'%s': %s," % (spacer*3, config_name, config_value))
                cms_text.append("%s}," % (spacer*2))
            cms_text.append("%s]," % spacer)
    cms_text.append("}")

    text.append("\n".join(cms_text))

    if config_data.bootstrap == 'yes':
        cms_templates = 'CMS_TEMPLATES_BOOTSTRAP'
    else:
        cms_templates = 'CMS_TEMPLATES'

    text.append("CMS_TEMPLATES = (\n%s%s\n%s%s\n)" % (
        spacer, "## Customize this",
        spacer, (",\n" + spacer).join(["('%s', '%s')" % item for item in getattr(vars, cms_templates)])))

    text.append("CMS_PERMISSION = %s" % vars.CMS_PERMISSION)
    text.append("CMS_PLACEHOLDER_CONF = %s" % vars.CMS_PLACEHOLDER_CONF)

    text.append("DATABASES = {\n%s'default':\n%s%s\n}" % (spacer, spacer*2, config_data.db_parsed))

    if config_data.filer:
        text.append("THUMBNAIL_PROCESSORS = (\n%s%s\n)" % (
        spacer, (",\n" + spacer).join(["'%s'" % var for var in vars.THUMBNAIL_PROCESSORS])))
    return "\n\n".join(text)


def setup_database(config_data):
    with chdir(config_data.project_directory):
        os.environ['DJANGO_SETTINGS_MODULE'] = (
            '{0}.settings'.format(config_data.project_name))
        try:
            import south
            subprocess.check_call([sys.executable, "-W", "ignore",
                                   "manage.py", "syncdb", "--all", "--noinput"])
            subprocess.check_call([sys.executable, "-W", "ignore",
                                   "manage.py", "migrate", "--fake"])
        except ImportError:
            subprocess.check_call([sys.executable, "-W", "ignore",
                                   "manage.py", "syncdb", "--noinput"])
            print("south not installed, migrations skipped")
        if not config_data.no_user:
            print("\n\nCreating admin user")
            subprocess.check_call([sys.executable, "-W", "ignore",
                                   "manage.py", "createsuperuser"])


def load_starting_page(config_data):
    """
    Load starting page into the CMS
    """
    with chdir(config_data.project_directory):
        os.environ['DJANGO_SETTINGS_MODULE'] = (
            '{0}.settings'.format(config_data.project_name))
        subprocess.check_call([sys.executable, "starting_page.py"])
        for ext in ['py', 'pyc', 'json']:
            try:
                os.remove('starting_page.%s' % ext)
            except OSError:
                pass
