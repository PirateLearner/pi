from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.db.models import Sum, Count

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
ZERO_VOTES_ALLOWED = getattr(settings, 'VOTING_ZERO_VOTES_ALLOWED', False)

UPVOTE = +1
DOWNVOTE = -1
if not ZERO_VOTES_ALLOWED:
    SCORES = (
        (+1, '+1'),
        (-1, '-1'),
    )
else:
    SCORES = (
        (+1, '+1'),
        (-1, '-1'),
        (0, '0'),
    )           


class VoteManager(models.Manager):
    def get_score(self, obj):
        """
        Get a dictionary containing the total score for ``obj`` and
        the number of votes it's received.
        
        Thus, it can be used to calculate the best rated objects in a very simplified scale.
        This isn't a very good rating function right now, because an object that has got a lot of up and downvotes
        is a reflection of its popularity, and then its score matters.
        """
        content_type = ContentType.objects.get_for_model(obj)
        result = self.filter(content_type=content_type,
                             object_id=obj._get_pk_val()).aggregate(
                                                                    score=Sum('vote'),
                                                                    num_votes=Count('vote'))
        #It may happen that there has been no voting on this object so far.
        if result['score'] is None:
            result['score'] = 0
        
        result['upvotes'] = self.get_upvotes(obj)
        result['downvotes'] = self.get_downvotes(obj)
        
        return result
    
    def record_vote(self, obj, vote, user):
        """
        Record a user's vote on a given object. Only allows a given user
        to vote once, though that vote may be changed.
        
        A zero vote indicates that any existing vote should be removed.
        """
        if vote not in (+1, 0, -1):
            raise ValueError('Invalid vote (must be +1/0/-1)')
        content_type = ContentType.objects.get_for_model(obj)
        # First, try to fetch the instance of this row from DB
        # If that does not exist, then it is the first time we're creating it
        # If it does, then just update the previous one
        try:
            vote_obj = self.get(voter=user, content_type=content_type, object_id=obj._get_pk_val())
            if vote == 0 and not ZERO_VOTES_ALLOWED:
                vote_obj.delete()
            else:
                vote_obj.vote = vote
                vote_obj.save()
                
        except ObjectDoesNotExist:
            #This is the first time we're creating it
            try:
                if not ZERO_VOTES_ALLOWED and vote == 0:
                    # This shouldn't be happening actually
                    return
                vote_obj = self.create(voter=user, content_type=content_type, object_id=obj._get_pk_val(), vote=vote)                        
            except:
                print '{file}: something went wrong in creating a vote object at {line}'.format(file=str('__FILE__'), line=str('__LINE__'))
                raise ObjectDoesNotExist    
        
        return vote_obj
    
    def get_top(self, model, limit=10, inverted=False):
        """
        Get the top N scored objects for a given model.

        Yields (object, score) tuples.
        """
        content_type= ContentType.objects.get_for_model(model)
        
        #Get a queryset of all the objects of the model. Get their scores
        results = self.filter(content_type=content_type).values('object_id').annotate(score=Sum('vote'))
        if inverted:
            results = results.order_by('score')
        else:
            results = results.order_by('-score')
        
        #We have a iterable list of objects of the requested model and their respective scores
        # Use in_bulk() to avoid O(limit) db hits.
        class_name = content_type.model_class()
        objects = class_name.objects.in_bulk([item['object_id'] for item in results[:limit]])

        # Yield each object, score pair. Because of the lazy nature of generic
        # relations, missing objects are silently ignored.
               
        for item in results[:limit]:
            id, score = item['object_id'], item['score']
                        
            if not score:
                continue
            
            if int(id) in objects:
                yield objects[int(id)], int(score)
        
    def get_bottom(self, model, limit):
        """
        Get the bottom (i.e. most negative) N scored objects for a given
        model.

        Yields (object, score) tuples.
        """
        return self.get_top(model=model, limit=limit, reversed=True)
    
    def get_for_user(self, obj, user):
        """
        Get the vote made on the given object by the given user, or
        ``None`` if no matching vote exists.
        """
        if not user.is_authenticated():
            return None
        content_object = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get(voter=user, content_type=content_object, object_id=obj._get_pk_val())
      
        except ObjectDoesNotExist:
            #print 'No vote by {user} on {object}'.format(user=user, object=obj)
            return None
            
        return vote
    
    def get_for_user_in_bulk(self, user):
        """
        Get all the objects on which the user has voted
        """
        if not user.is_authenticated():
            return None
        #TODO: This one will need more refinement.
        return self.filter(voter=user)
        
    
    def get_upvotes(self, obj):
        """
        Gets the number of upvotes made on the object by all users
        """
        content_type = ContentType.objects.get_for_model(obj)
               
        votes = self.filter(content_type=content_type, object_id=obj._get_pk_val(), vote__exact=UPVOTE).aggregate(upvotes=Sum('vote'))
                
        if votes['upvotes'] is None:
            votes['upvotes'] = 0

        return votes['upvotes']
    
    def get_downvotes(self, obj):
        """
        Gets the number of downvotes on the object by all users
        """
        content_type = ContentType.objects.get_for_model(obj)
        
        votes = self.filter(content_type=content_type, object_id=obj._get_pk_val(), vote__exact=DOWNVOTE).aggregate(downvotes=Sum('vote'))
        
        if votes['downvotes'] is None:
            votes['downvotes'] = 0
            
        return -votes['downvotes']
    
class Vote(models.Model):
    
    #The ID of the object on which vote was cast
    content_type = models.ForeignKey(ContentType, verbose_name="Content Type", related_name="content_type_set_for_voting")
    object_id = models.TextField(_('object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    #Vote made by User
    voter = models.ForeignKey(User, related_name="voted")

    #Vote value
    vote = models.SmallIntegerField(choices=SCORES)
    
    #For weighted treatement of experienced user's opinion    
    score = models.SmallIntegerField(default=0)
    
    vote_date = models.DateTimeField(auto_now_add=True)
    vote_modified = models.DateTimeField(auto_now=True)
  
    objects = VoteManager()
  
    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1
    
    def __unicode__(self):
        return str(self.vote)
    
    def __str__(self):
        return str(self.vote)
    
    class Meta:
        app_label = 'voting'
    