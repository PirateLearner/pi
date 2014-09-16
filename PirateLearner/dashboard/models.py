from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from allauth.socialaccount.models import SocialAccount
import hashlib
# Create your models here.

rlevel = (
    ('begineer','begineer'),
    ('expert','expert'),
    ('pro','pro'),
    ('pirate','pirate')
)
""""
class Profile(models.Model):
    user = models.ForeignKey(User,related_name='profile')
    question_asked = models.IntegerField(default=0)
    question_answered = models.IntegerField(default=0)
    public_notes = models.IntegerField(default=0)
    private_notes = models.IntegerField(default=0)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    social_score = models.IntegerField(default=0)
    invitation_score = models.IntegerField(default=0)
    reputation_score = models.IntegerField(default=0)
    reputation_level = models.CharField(choices=rlevel,max_length=10)

    class Meta:
        db_table = 'userprofile'
        verbose_name = 'Profile'


    @property
    def get_upvote_count(self):
        return self.upvote_count

    @property
    def get_downvote_count(self):
        return self.downvote_count

    @property
    def get_reputation_level(self):
        return self.reputation_level

    @property
    def get_private_notes_count(self):
        return self.private_notes

    @property
    def get_public_notes_count(self):
        return self.public_notes

    @property
    def get_reputation_score(self):
        return self.reputation_score
        
"""

OCCUPATION = ((0, 'Student'),
                 (1, 'IT-Professional'),
                 (2, 'Telecom-Engineer'),
                 (3, 'Achedmic'),
                 (4, 'Algorithm'),
                 (5, 'Analog'),
                 (6, 'Digital'))
 
GENDERS = (
           ('M','Male'),
           ('F','Female'),
           )

class UserProfile(models.Model):
    """
    User profile populated using social account from Facebook, Google and Twitter respectively.
    """
    user = models.OneToOneField(User, related_name='profile')
    address = models.TextField(null=True)
    occupation = models.IntegerField(choices=OCCUPATION,blank=True,null=True)
    website = models.CharField(max_length = 100,blank=True,null=True)
    interest = TaggableManager(blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(choices=GENDERS, 
                               max_length=20)
    
    def __unicode__(self):
        return "{}'s profile".format(self.user.username)
 
    class Meta:
        db_table = 'user_profile'
    
    
    def _get_social_account(self):
        """
        Return the social account object of Facebook, Google and Twitter in that order.
        """
        account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        if len(account_uid):
            return account_uid[0]

        account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
        if len(account_uid):
            return account_uid[0]

        account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='twitter')
        if len(account_uid):
            return account_uid[0]
        
    
    def get_avatar_url(self):
        """
        Return the avatar of social account Facebook, Google and Twitter in that order
        todo: return default avatar if no social account is found.
        """
        return self._get_social_account().get_avatar_url()
    
    def get_username(self):
        """
        Return the username of social account Facebook, Google and Twitter in that order
        todo: return default avatar if no social account is found.
        """
        return self._get_social_account().extra_data['username']


    def get_first_name(self):
        """
        Return the first name from social account Facebook, Google and Twitter in that order
        todo: return default first name from User model if no social account is found.
        """
        return self._get_social_account().extra_data['first_name']


    def get_last_name(self):
        """
        Return the last name from social account Facebook, Google and Twitter in that order
        todo: return default last name from User model if no social account is found.
        """
        return self._get_social_account().extra_data['last_name']

    def get_gender(self):
        """
        Return the gender from social account Facebook, Google and Twitter in that order
        todo: return default last name from User model if no social account is found.
        """
        return self._get_social_account().extra_data['gender']

    def get_email(self):
        """
        Return the email of social account Facebook, Google and Twitter in that order
        todo: return default last name from User model if no social account is found.
        """
        return self._get_social_account().extra_data['email']


    def get_occupation(self):
        return self.occupation

    def get_address(self):
        return self.address                        

    def get_website(self):
        return self.website                        
 
    def get_interest(self):
        return self.interest.all()                        

    def get_birthday(self):
        return self.date_of_birth  
                      

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
