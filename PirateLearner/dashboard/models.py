from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from allauth.socialaccount.models import SocialAccount
import hashlib
from django.utils import timezone
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
    occupation = models.IntegerField(choices=OCCUPATION,default = 0)
    website = models.CharField(max_length = 100,blank=True,null=True)
    interest = TaggableManager(blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(choices=GENDERS, 
                               max_length=20)
    signin_date = models.DateTimeField('date created', auto_now_add=True)
    
    def __unicode__(self):
        return "{}'s profile".format(self.user.username)
 
    class Meta:
        db_table = 'user_profile'
    
    
    def _get_social_account(self,provider=None):
        """
        Return the social account object of Facebook, Google and Twitter in that order if provier is None else return the provider account.
        """
        if provider != None:
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider=provider)
            if len(account_uid):
                return account_uid[0]
            else:
                return None
            
        
        account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        if len(account_uid):
            return account_uid[0]

        account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
        if len(account_uid):
            return account_uid[0]

        account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='twitter')
        if len(account_uid):
            return account_uid[0]

    
    def is_social_account_exist(self,provider):
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider=provider)
            if len(account_uid):
                return True
            else:
                return False
        
    
    def get_avatar_url(self,provider=None):
        """
        Return the avatar of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default avatar if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.get_avatar_url()
        else:
            return "{{ STATIC_URL }}images/default-avatar.png"
    
    def get_username(self,provider=None):
        """
        Return the username of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default avatar if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.extra_data['username']
        else:
            return "John Doe"


    def get_name(self ,provider=None):
        return "{0} {1}".format(self.get_first_name(provider),self.get_last_name(provider))

    def get_first_name(self,provider=None):
        """
        Return the first name from social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default first name from User model if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.extra_data['first_name']
        else:
            return "John"


    def get_last_name(self,provider=None):
        """
        Return the last name from social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default last name from User model if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.extra_data['last_name']
        else:
            return "Doe"

    def get_gender(self,provider=None):
        """
        Return the gender from social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default last name from User model if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.extra_data['gender']
        else:
            return "Male"

    def get_email(self,provider=None):
        """
        Return the email of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default email  if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.extra_data['email']
        else:
            return "jondo@example.com"


    def get_social_url(self,provider=None):
        """
        Return the social url of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default blank  if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.extra_data['link']
        else:
            return ""
       
    def get_provider_name(self,provider=None):
        """
        Return the provider name of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default blank  if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            return profile.provider
        else:
            return provider
    

    def get_occupation(self):
            tmp = dict(OCCUPATION)
            return tmp[self.occupation]

    def get_address(self):
        return self.address                        

    def get_website(self):
        return self.website                        
 
    def get_interest(self):
        return self.interest.all()                        

    def get_birthday(self):
        return self.date_of_birth  
    
    def get_signin_time(self):
        return self.signin_date

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
