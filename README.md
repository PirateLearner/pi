pi
==

Python Based CMS Framework


Install Instructions
=====================

The following instructions should help you setup 'pi' on a linux machine (As done on Ubuntu 12.04)

Prerequisites:
==============

MySQL [if you're not using integrated sqlite db]
-----
   It can be installed using {apt-get install } method.
   libmysqlclient-dev will be required, in case it is not installed before.

pip
---
   Installed using the get_pip.py file from their webserver. 
      (sudo python2.7 get_pip.py)
virtualenv
----------
   (sudo pip install virtualenv)

python-MySQLdb connector
------------------------
   sudo apt-get install python-mysqldb

Optionally(for developers)
--------------------------
   Install eclipse and 'pydev' plugin on eclipse

Clone this git repository 
-------------------------
and its auxilliary repo for static files - PirateLearnerStatic(That contains most static files which you might not want to use in your projects), to a folder from where you'd be running your site. [Our's is ~/git/ as cloned directly through eclipse]

Install Steps:
==============
1. Create a virtual environment where all libraries will be installed to:
   virtualenv env
2. Activate the newly created virtualenv box
   source env/bin/activate
3. Go to the installation folder where the repositories were cloned
   cd ~/git/pi
4. Install the dependencies [Django and other modules will be installed] Note: cmsplugin_contact does not install its latest version and thus gives an error on running. This can be resolved by removing cmsplugin_contact from the requirement.txt and manually installing it later.
   pip install -r requirement.txt
5. Edit settings.py in PirateLearner/PirateLearner. Following are the variables to lookout for [The first 7 are significant, rest all are site specific addons]:
   STATIC_ROOT
   STATIC_URL
   MEDIA_ROOT
   MEDIA_URL
   ALLOWED_HOSTS
   TIMEZONE
   LANGUAGE_CODE
   DISQUS_API_KEY
   DISQUS_API_WEBSITE_SHORTNAME
   MATHJAX
   CKEDITOR_UPLOAD_PATH
6. Install MySQL Connector (We already installed one using sudo apt-get install python-mysqldb; apparently, it was not detected)
    pip install MySQL-python
7. Create the database 'sampledb' along with encoding info (change name appropriately in the settings.py file too) from MySQL prompt
   >>> CREATE DATABASE sampledb 
8. Populate schema in DB
   python manage.py syncdb --all
   This should create various tables related to the site in the database.

Now, try running the test server :
----------------------------------

python manage.py runserver


From the browser, visit: 127.0.0.1:8000

If everthing went well, it should show the welcome page of DjangoCMS [We've taken that as base for now, will move out of it eventually]

127.0.0.1:8000/admin/ should take you to the admin site where you would see the CMS as well as blogging apps.

For starters, add a home page from the cms app, and to it, add a blogging plugin:

Currently there are two plugins, 'recent entries', and 'sections view'

Recent Entries Plugin can be configured to show recently published entries from a particular parent section (on any level) created in the blogging app. if not set to anything, it shows the most recent entries from overall content.

Section Plugin allows you to view various Sections and subsections that have been created in the blogging app.


So far so good. Feel free to contact us in case of doubt, or if you want to suggest improvements, report bugs, or want to join in. We're looking for contributors :-)


This last command is to install modules into a path different from default configured path:
-------------------------------------------------------------------------------------------

export TEMP=$HOME/tmp
cd pi/piratelearner
pip2.7 install --target=$PWD/lib/python2.7 --install-option="--install-scripts=$PWD/bin" --install-option="--install-lib=$PWD/lib/python2.7" -r requirement.txt

Note: Regarding RestFrameworkGenericRelations
---------------------------------------------

This module will cause errors while using the REST API for annotations module and cause the code to break. To fix the issue: Please replace the field_to_native method code segment
in generic_relations/relations.py by:


    def field_to_native(self, obj, field_name):
        """
        Delegates to the `to_native` method of the serializer registered
        under obj.__class__
        """
        value = super(GenericRelatedField, self).field_to_native(
            obj, field_name)
        if value:
            serializer = self.determine_deserializer_for_data(value)

            # Necessary because of context, field resolving etc.
            serializer.initialize(self.parent, field_name)
            return serializer.to_native(value)

Note: Upgrading blogging plugin schema     
--------------------------------------

ALTER TABLE `blogging_latestentriesplugin` ADD COLUMN `template` varchar(255) NOT NULL DEFAULT 'blogging/plugin/plugin_teaser.html';




