from django.db import models
from django.contrib.auth.models import User
# Create your models here.

rlevel = (
    ('begineer','begineer'),
    ('expert','expert'),
    ('pro','pro'),
    ('pirate','pirate')
)

class Profile(models.Model):
    user = models.ForeignKey(User,related_name='user_name')
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