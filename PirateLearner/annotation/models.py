from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from django.core import urlresolvers

from django_comments.models import BaseCommentAbstractModel
# Create your models here.

privacy_levels = {'private':0, 'author':1, 'group':2, 'public':3}

class AnnotationManager(models.Manager):

    def in_moderation(self):
        """
        QuerySet for all comments currently in the moderation queue.
        """
        #The condition is wrong.
        return self.get_queryset().filter(privacy_override_flag=True)

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs
    
    '''
    Called like .objects.which_are_public() or .objects.which_are_mine etc ;P
    '''
    def which_are_public(self):
        pass
    
    def which_are_mine(self):
        pass
    
    def which_are_private(self):
        pass


class Annotation(BaseCommentAbstractModel):
    '''@class Annotation
    Extends a BaseCommentAbstractModel to utilize generic keys and decouple it from 
    any specific model.
    Two fields provided by it are: Content_type and Object_Pk
    
    Object_Pk must point to the 'id' in case of contet_type being 'BlogContent'
    
    Additionally, site_id is also used. For our specific use, it was not required.
    But, for a generic case, it may come in handy and hence, is being kept.    
    '''
    
    #Paragraph ID on which this comment was posted. It should necessarily exist, if not, the annotation
    #will be collected in the bottom. 
    paragraph_id = models.PositiveIntegerField(null=False)
    
    body = models.TextField()
    '''
    Annotations can be written only by logged in users. If the user cannot afford 
    to make himself and his interest in reading known, alas, we cannot help him in
    case of making annotations. It is also to prevent hit and run comments by people
    under anonymity.
    '''
    user = models.ForeignKey(DjangoUser, null=False, verbose_name=_('user'), related_name = "annotations")
    
    #Sharing and repurcussion
    privacy = models.PositiveSmallIntegerField(default = privacy_levels['author'])
    privacy_override_flag = models.BooleanField(default = False)
    shared_with = models.ManyToManyField(DjangoUser, through='Annotation_share_map', null=True)
    
    
    #Metadata about the annotation:
    submit_date = models.DateTimeField(_('date/time submitted'), auto_now_add=True)
    last_modify_date = models.DateTimeField(_('last edited on'), auto_now = True)
    
    objects = AnnotationManager()
    
    def __unicode__(self): #Python2
        return self.body
    
    def __str__(self): #Python3
        return "%s: %s..." %(self.name, self.body[:50])
    
    class Meta:
        app_label = 'annotation'
        ordering = ('last_modify_date',)
        verbose_name = _('annotation')
        verbose_name_plural = _('annotations')
        permissions = [("can_moderate", "Can moderate annotations")]
    
    
    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return urlresolvers.reverse(
            "annotation:annotation-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )
        
    def _get_userinfo(self):
        """
        From Comments:
        Get a dictionary that pulls together information about the poster
        safely.

        This dict will have ``name``, ``email``, and ``url`` fields.
        """
        if not hasattr(self, "_userinfo"):
            userinfo = {
                "name": '',
                "email": '',
                "url": ''
            }
            if self.user_id:
                u = self.user
                if u.email:
                    userinfo["email"] = u.email

                # If the user has a full name, use that for the user name.
                # However, a given user_name overrides the raw user.username,
                # so only use that if this comment has no associated name.
                if u.get_full_name():
                    userinfo["name"] = self.user.get_full_name()
                else:
                    userinfo["name"] = u.get_username()
            self._userinfo = userinfo
        return self._userinfo
    userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)
    
    def _get_name(self):
        return self.userinfo["name"]
    
    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "\
                                   "user and thus the name is read-only."))
        self.user_name = val
    name = property(_get_name, _set_name, doc="The name of the user who posted this comment")
    

    def _get_email(self):
        return self.userinfo["email"]
    email = property(_get_email, doc="The email of the user who posted this comment")
    
    
    def _get_url(self):
        return self.userinfo["url"]

    def _set_url(self, val):
        self.user_url = val
    url = property(_get_url, _set_url, doc="The URL given by the user who posted this comment")

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.user or self.name,
            'date': self.submit_date,
            'body': self.body,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d
    
    def _set_privacy_level(self, privacy_level= privacy_levels['author']):
        '''@_set_privacy_level
        This method is called internally everytime an annotation is saved.
        
        Revision: Rather than actually change the privacy level as set by user,
        it would be much better if the combined condition of Blocked Flag not been
        set and Annotation being of desired privacy level be used instead.        
        This would save us the trouble of tracking the desired and actual privacy levels
        in two fields, in case the moderator unblocks the annotation.
        
        It checks if the user's privacy flag has been overridden by the moderator
        This happens if people have flagged it as inappropriate and the moderator
        has removed the annotation from public view. The author may change the comment 
        but not reset the privacy. For that, he must talk to the moderator.
        '''
        #if self.privacy_override_flag:
        #   self.privacy = privacy_levels['private']
        #   return
        self.privacy = privacy_level
    
    def unlock_annotation(self):
        '''@unlock_annotation
        Can be used by the moderator or anyone with escalated privilege to unlock 
        the annotation privacy override flag.        
        '''
        self.privacy_override_flag = False
    
    def check_override(self):
        '''@check_override
        Returns true if the annotation has been blocked for public view, false otherwise        
        '''
        if self.privacy_override_flag:
            return True
        return False
    
    @classmethod
    def _sanitize_text(cls,body):
        '''@_sanitize_text
        Returns a DB safe textfield which may be saved in the DB. This function should
        call into the sanitization library rather than implementing it on its own. 
        Thus the same sanitization library may be used throughout the project.
        '''
        pass
    
    @classmethod
    def get_annotation(cls, annotation=None, post=None, user=None, privacy=privacy_levels['public']):
        '''@get_annotation
        A Public Classmethod to fetch the entries from DB.
        '''
        #Setup Query as an array of Q filters which we can recursively append late
        #update Don't be silly!
        #Setup Query as a chainrule of filters. The queries are not performed until used,
        # since Django uses Lazy queries, so we don't need to indulge in 
        
        #Initially, we assume we want everything.
        queryset = cls.objects.all()
        
        #Then, we start filtering based on input provided
        if annotation is not None and isinstance(annotation, (int,long)):
            #In python3, use isinstance(annotation, int)
            #A specific ID of annotation has been requested. It can be by the author, or moderator
            queryset = cls.objects.get(pk=annotation)
            return queryset
    
        if post is not None and isinstance(annotation, (int, long)): 
            #Very burdensome method to have to type it again and again. Can we have a lambda or something?
            #for foreign key elements, append a trailing _id to it
            try:
                queryset = queryset.filter(node_id = post)
            except TypeError:
                print 'Invalid Foreign Key node_id: not a valid member, or foreign key'
                return None
        
        if user is not None and isinstance(user, (int,long)):
            #User ID has been provided. Note thatwe're not passing User instance
            #since someone might be stalking, or perusing someone else's annotations ;)
            try: 
                queryset = queryset.filter(author_id = user)
            except TypeError:
                print 'Invalid Foreign Key author_id: not a valid member, or foreign key'
                return None
        
        if privacy not in privacy_levels:
            #if some invalid privacy level has been passed, use default
            privacy = privacy_levels['public']
            
        queryset = queryset.filter(privacy__exact = privacy)
        
        #All set, now return the queryset. Now, should this go into a manager?
        return queryset        
        
    def dispatch_notification(self, request):
        '''@dispatch_notification
        It should check if the annotation has been shared with someone and send them a message
        Send a signal out.
        '''
        if request.POST.get('share_with', None) is not None:
            pass #TODO
                    
    
    def save_annotation(self, request):
        '''@save_annotation
        It must generate pre-save and post save signals later, and call into
        dispatcher if the post have been shared with someone
        '''
        #first sanitize text
        self.body = self._sanitize_text(self.body)
        self.author = request.user
        try:
            self.node = request.POST.get('node')
        except:
            return None #Must return a valid error
        '''
        A notification must be sent to shared users only if it is being created 
        for the first time. Otherwise, it must silently save. 
        '''
        if request.POST.get('share_with', None) is not None:
            if request.POST.get('op', None) is not None and request.POST.get('op', None) == 'create':
                #If op is create , it is freshly created
                self.dispatch_notification()
            self.save()
            
    def save(self, *args, **kwargs):
        super(Annotation, self).save(*args, **kwargs)
    
    def get_permalink(self):
        '''@get_permalink
        Generate a permalink to this annotation. Note that a permalink can 
        be created to private annotations also, but will not be visible to others
        '''
        #Construct a permalink from the node id, paragraph id and self.id for this annotation
        #soemthing like this: taken from comments framework
        return urlresolvers.reverse(
                                    "comments-url-redirect",
                                    args=(self.content_type_id, self.object_pk)
                                    )

class Annotation_share_map(models.Model):
    '''@class Annotation_share_map
    Maintains a map of which annotation has been shared by the user with which of his friends, if applicable.
    Notification about the sharing should be sent to each person only once, even if the user edits the 
    comment later
    '''
    user = models.ForeignKey(DjangoUser)
    annotation = models.ForeignKey(Annotation)
    notified_flag = models.BooleanField(default = False)
    
    class Meta:
        app_label = 'annotation'


def get_annotation_for_model(content_object, include_moderated=False):
    """
    Return the QuerySet with all annotations for a given model.
    """
    qs = Annotation.get_model().objects.for_model(content_object)

    if not include_moderated:
        qs = qs.filter(privacy_level = privacy_levels['public'])

    return qs