from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from allauth.socialaccount.models import SocialAccount
import hashlib
from django.utils import timezone

from PirateLearner.models import BaseContentClass
from django.conf import settings
from django.core.urlresolvers import reverse

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

class UserProfile(BaseContentClass):
    """
    User profile populated using social account from Facebook, Google and Twitter respectively.
    """
    user = models.OneToOneField(User, related_name='profile',on_delete = models.CASCADE)
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
            
        try:
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
            if len(account_uid):
                return account_uid[0]
    
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
            if len(account_uid):
                return account_uid[0]
    
            account_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='twitter')
            if len(account_uid):
                return account_uid[0]
        except:
            return None
        else:
            return None
    
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
            return settings.STATIC_URL + "images/add_new.png"
    
    def get_profile_name(self):
        name  = self.get_first_name(None)
        if name is None:
            name = self.get_username(None)
        
        return name
    
    def get_username(self,provider=None):
        """
        Return the username of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default avatar if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_username(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_username(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_username(profile)
            else:
                return self.user.username
        else:
            return self.user.username


    def get_name(self ,provider=None):
        return "{0} {1}".format(self.get_first_name(provider),self.get_last_name(provider))

    def get_first_name(self,provider=None):
        """
        Return the first name from social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default first name from User model if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_fname(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_fname(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_fname(profile)
            else:
                return self.user.first_name
        else:
            return self.user.first_name
    
    def get_last_name(self,provider=None):
        """
        Return the last name from social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default last name from User model if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_lname(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_lname(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_lname(profile)
            else:
                return self.user.last_name

        else:
            return self.user.last_name

    def get_gender(self,provider=None):
        """
        Return the gender from social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default last name from User model if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'twitter':
                return "---"
            gender =  profile.extra_data.get('gender',None)
            if gender is None:
                return self.gender
            else:
                return gender
        else:
            return "---"

    def get_email(self,provider=None):
        """
        Return the email of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default email  if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            if self.get_provider_name(profile.provider) == 'twitter':
                return self.user.email
            return profile.extra_data['email']
        else:
            return self.user.email


    def get_social_url(self,provider=None):
        """
        Return the social url of social account Facebook, Google and Twitter in that order, if provider is None.
        todo: return default blank  if no social account is found.
        """
        profile = self._get_social_account(provider)
        if profile != None:
            print profile.extra_data
            if self.get_provider_name(profile.provider) == 'facebook':
                return self._get_fb_link(profile)
            elif self.get_provider_name(profile.provider) == 'google':
                return self._get_google_link(profile)
            elif self.get_provider_name(profile.provider) == 'twitter':
                return self._get_tw_link(profile)
            else:
                return ""
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
    
    def get_profile_page(self):
        return reverse('dashboard:dashboard-profile', kwargs={'user_id': self.user.id})

    """
    Private functions for retrieving the fname, lname, email etc. from GooGle, Facebook and twitter
    TODO define these functions for twitter also
    """    
    def _get_google_fname(self,profile):
        return str(profile.extra_data['name']).split(' ')[0].encode('utf-8')
    
    def _get_google_lname(self,profile):
        return profile.extra_data['family_name'].encode('utf-8')

    def _get_google_email(self,profile):
        return profile.extra_data['email'].encode('utf-8')

    def _get_google_email(self,profile):
        return profile.extra_data['email'].encode('utf-8')

    def _get_google_username(self,profile):
        return profile.extra_data['given_name'].encode('utf-8')

    def _get_google_link(self,profile):
        return profile.extra_data['link']

    def _get_fb_fname(self,profile):
        return profile.extra_data['first_name'].encode('utf-8')
    
    def _get_fb_lname(self,profile):
        return profile.extra_data['last_name'].encode('utf-8')

    def _get_fb_email(self,profile):
        return profile.extra_data['email'].encode('utf-8')

    def _get_fb_username(self,profile):
        return profile.extra_data['name'].encode('utf-8')

    def _get_fb_link(self,profile):
        return profile.extra_data['link']
    
    def _get_tw_fname(self,profile):
        return str(profile.extra_data['name']).split(' ')[0].encode('utf-8')

    def _get_tw_lname(self,profile):
        return str(profile.extra_data['name']).split(' ')[-1].encode('utf-8')

    def _get_tw_username(self,profile):
        return profile.extra_data['screen_name'].encode('utf-8')

    def _get_tw_link(self,profile):
        return  "//twitter.com/" + str(profile.extra_data['screen_name'])

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
