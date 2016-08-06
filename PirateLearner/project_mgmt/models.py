"""
Models for Project Management :
1. Project
2. Apps
3. Tasks
4. Features

Project will have following fields:
a) Owner
b) contributors
c) name 
d) slug
e) description
f) start date
g) hidden (Boolean)

Apps:
a) Project (many to many)
b) name
c) contibutors
d) slug
e) description
f) start date

Task:
a) Apps (Unique)
b) name 
c) owner
d) Start date
e) status
f) priority
g) complexity
h) estimated_man_hour
i) applied_man_hour
j) progress
k) completion_date

Project will calculate various values from APPS and Tasks involved and these are --
a) Project estimation
b) Progress report


Features will be disjoint from project and Apps but it will depend upon the tasks related to it. It wil derive it's 
completion report from the task involved.

"""

from django.db import models
from django.conf import settings as global_settings
if 'cms' in global_settings.INSTALLED_APPS:
    from cms.models.pluginmodel import CMSPlugin
    from cms.models import Page
from django.core.validators import MinValueValidator, MaxValueValidator

from PirateLearner.models import BaseContentClass

from PirateLearner import settings
# Create your models here.
"""
class Project(models.Model):
    owner = models.ForeignKey(User, related_name='project_ownership_set')
    contibutor = models.ManyToManyField(User, related_name='project_membership_set', blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(db_index=True)
    hidden = models.BooleanField(db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True)
"""

"""

class ProjectTime(models.Model):
"""
"""
    Make entry in this table when Any App related to the project submitted. put the end value when completed and calculate the _time
    
"""
"""
    creation_date = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    project = models.ForeignKey(Project)
    _time = models.DecimalField(max_digits=4, decimal_places=2, null=True, editable=False)


class App(models.Model):
    projects = models.ManyToManyField(Project, related_name='app_projects_set')
    contibutor = models.ManyToManyField(User, related_name='app_membership_set', blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
class Task(models.Model):
    COMPLETED = 'CP'
    STARTED = 'ST'
    PENDING = 'PD'
    WISHLIST = 'WL'
    TASK_STATUS = (
        (COMPLETED, 'Task Completed'),
        (STARTED, 'Started working'),
        (PENDING, 'Yet to be started'),
        (WISHLIST, 'Submit for confirmation'),
    )
    LOW_COMPLEXITY = 'LO'
    MODERATE_COMPLEXITY = 'MOD'
    HIGH_COMPLEXITY = 'HI'
    COMPLEXITY = (
                  (LOW_COMPLEXITY,'Low Complexity'),
                  (MODERATE_COMPLEXITY,'Moderate Complexity'),
                  (HIGH_COMPLEXITY, 'High Complexity')
                  )
    app = models.ForeignKey(App, related_name='task_app_set')
    owner = models.ForeignKey(User, related_name='task_owner_set', blank=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=60, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=2,
                                      choices=TASK_STATUS,
                                      default=WISHLIST)
    priority = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(10)],default=0) # range from low priority to high priority 0-10
    complexity = models.CharField(max_length=2,
                                      choices=COMPLEXITY,
                                      default=MODERATE_COMPLEXITY)
    completion_date = models.DateTimeField(blank=False)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    applied_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
"""
if 'cms' in global_settings.INSTALLED_APPS:     
    class WishlistPlugin(CMSPlugin):
        completed_number = models.IntegerField(default= '2')
        started_number = models.IntegerField(default= '1')
        pending_number = models.IntegerField(default= '2')
     
        def __unicode__(self):
            return 'WishlistPlugin'
        
        def get_suggestion_url(self):
            #page = Page.objects.get(title='Contact Us') or None
            from django.core.urlresolvers import reverse
            return (settings.DOMAIN_URL+'en/contact-us/?contact_type=Feature')

