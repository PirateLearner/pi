from django.test import TestCase

from voting.models import Vote, UPVOTE, DOWNVOTE
from blogging.models import BlogContent

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework.authtoken.models import Token

from rest.serializers import VoteSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

import json 
from unittest import skip
# Create your tests here.

class VotingTests(TestCase):
    
    fixtures = ['fixtures.json',]
    
    def setUp(self, *args, **kwargs):
        #create 2 new users
        #load the blogging post into a variable
        self.author = User.objects.get(pk="1")
        #token = Token.objects.create(user=self.author)
        #token.save()
        self.user1 = User.objects.create_user(username="User1", email="user1@users.com", password="user1")
        token = Token.objects.create(user=self.user1)
        token.save()
        self.user2 = User.objects.create_user(username="User2", email="user2@users.com", password="user2")

        self.article = BlogContent.objects.get(pk="1")
        
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        #self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        
    def _create_votes(self, votes=[+1,+1]):
        Vote.objects.create(object_id = self.article._get_pk_val(), 
                            content_type = ContentType.objects.get_for_model(self.article), 
                            voter = self.user1,
                            vote = votes[0])
            
        
        Vote.objects.create(object_id = self.article._get_pk_val(), 
                            content_type = ContentType.objects.get_for_model(self.article), 
                            voter = self.user2,
                            vote = votes[1])
            
    
    def _create_model_vote(self, user=None, vote=UPVOTE):
        vote_obj = Vote.objects.create(object_id = self.article._get_pk_val(), 
                                        content_type = ContentType.objects.get_for_model(self.article), 
                                        #content_object = ContentType.objects.get_for_model(self.article),
                                        voter = user,
                                        vote = vote)
        return vote_obj    
        
    def _require_login(self, username, password):
        self.client.login(username=username, password=password)
        
    def _logout(self):
        self.client.logout()

class ModelTests(VotingTests):        
    def test_vote_model(self):
        vote = Vote()
        vote.object_id = self.article._get_pk_val()
        vote.content_type = ContentType.objects.get_for_model(self.article)
        #vote.content_object = ContentType.objects.get_for_model(self.article)
        
        vote.voter = self.user1
        vote.vote = UPVOTE
        
        vote.save()
        
        vote_obj = Vote.objects.all()[0]
        self.assertEqual(vote_obj._get_pk_val(), vote._get_pk_val(), "Primary Keys do not match")
        self.assertEqual(vote.vote, vote_obj.vote, "Vote value does not match")
        
    def test_record_vote(self):
        vote = Vote.objects.record_vote(self.article, DOWNVOTE, self.user1)        
        
        
        vote_obj = Vote.objects.all()[0]
        self.assertEqual(vote_obj._get_pk_val(), vote._get_pk_val(), "Primary Keys do not match")
        self.assertEqual(vote.vote, vote_obj.vote, "Vote value does not match")
            
    def test_load_votes(self):
        self._create_votes([UPVOTE,DOWNVOTE])
        
        votes = Vote.objects.all()
                
        self.assertEqual(votes.count(), 2)
        self.assertEqual(votes[0].vote, UPVOTE, "UPVOTE not found")
        self.assertEqual(votes[1].vote, DOWNVOTE, "DOWNVOTE not found")
        
    def test_get_upvotes(self):
        self._create_votes((UPVOTE, UPVOTE))
        '''
        votes = Vote.objects.all()
        
        for vote in votes:
            print '\n'
            print vote.object_id, '\n',vote.content_type._get_pk_val(), '\n',vote.content_object, '\n',vote.voter, '\n',vote.vote
        '''
        vote = Vote.objects.get_upvotes(obj=self.article)
        #print 'upvotes: {upvotes}'.format(upvotes=vote)
        
        self.assertEqual(vote, 2)
    
    def test_get_downvotes(self):
        self._create_votes((DOWNVOTE, UPVOTE))
        
        vote = Vote.objects.get_downvotes(obj=self.article)
        #print 'upvotes: {upvotes}'.format(upvotes=vote)
        
        self.assertEqual(vote, 1)
        
    def test_get_top(self):
        self._create_votes((UPVOTE, UPVOTE))
        
        values = Vote.objects.get_top(model=self.article)
        #print 'upvotes: {upvotes}'.format(upvotes=vote)
        for obj,value in values:
            self.assertEqual(obj, self.article, "Article ID is not correct")
            self.assertEqual(value, 2, "Score is not 2")
        #self.assertEqual(vote.count(), 1)
        
    def test_get_for_user(self):
        self._create_votes((UPVOTE, UPVOTE))
        
        
        self._require_login('user1', 'user1')
        vote = Vote.objects.get_for_user(self.article, self.user1)
        self.assertEqual(vote.vote, UPVOTE, "We upvoted it, but got {vote} instead".format(vote=vote))
        self._logout()
        
        self._require_login('craft', 'craft')
        vote = Vote.objects.get_for_user(self.article, self.author)
        self.assertIsNone(vote,"Did not expect an instance")
        self._logout()
        
        '''
        vote = Vote.objects.get_for_user(self.article, self.user2)
        self.assertIsNone(vote,"Did not expect an instance. Did not login")
        '''
        
    def test_for_user_in_bulk(self):
        self._create_votes((UPVOTE, UPVOTE))
        
        self._require_login('user1', 'user1')
        votes = Vote.objects.get_for_user_in_bulk(self.user1)
        #print votes
        #self.assertEqual(vote.vote, UPVOTE, "We upvoted it, but got {vote} instead".format(vote=vote.vote))
    
    
class ViewTests(VotingTests):
    
    def test_create_serializer_class(self):
        vote = self._create_model_vote(user=self.user1, vote= UPVOTE)
        
        obj = VoteSerializer(vote)
        #print(obj.data)
        
        json_value = JSONRenderer().render(obj.data)
        #print '\n', json_value, '\n'
        
    @skip('skipping')
    #This is just for exploratory purpose
    def test_create_serializer_instance(self):
        obj = VoteSerializer()
        print(obj)
    
    def test_view_annotations(self):
        vote = self._create_model_vote(user=self.user1, vote=UPVOTE)
        
        response = self.client.get('/voting/votes/')
        
        response_json = json.loads(response.content.decode())
        #First element must be our vote. We made just one.
        self.assertEqual(vote._get_pk_val(), response_json[0].get('id'), "Returned list did not contain our vote")
    

    def test_create_vote(self, content=None):
        #use test client to POST a request
        self._require_login('user1','user1')
        string_data = {
                    'content_type': '9',
                    'object_id':'1',
                    'vote':'1',
                    }
        json_data = json.dumps(string_data)
        response =  self.client.post(
            '/voting/votes/',
            content_type='application/json',
            data = json_data,
         )
        
        #print response.content.decode()
        
        resp = json.loads(response.content.decode())
        
        vote = Vote.objects.all()[0]
        self.assertEqual(vote._get_pk_val(), resp.get('id'), "ID's do not match")
    
    def _create_vote(self, content=None, user=None, password=None):
        #use test client to POST a request
        self._require_login(user, password)
        #print(self.user.is_authenticated()) # returns True
        string_data = {
                    'content_type': content['content_type'],
                    'object_id':content['object_id'],
                    'vote': content['vote'],
                    }
        
        json_data = json.dumps(string_data)
        return self.client.post(
            '/voting/votes/',
            content_type='application/json',
            data = json_data,
         )
    
    
    def test_upvote(self):
        response = self._create_vote(content={
                    'content_type': 9,
                    'object_id':1,
                    'vote':1,
                    },
                    user='user1', 
                    password='user1')
               
        #Expect a JSON object in response           
        resp = json.loads(response.content.decode())
            
        self.assertEqual(Vote.objects.all().count(), 1)
        vote = Vote.objects.all()[0]
        self.assertEqual(vote._get_pk_val(), resp.get('id'), "ID's do not match")
        self.assertEqual(int(UPVOTE), resp.get('vote'), "Vote Value doesn't match")
        
        
    #@skip('skipping')
    def test_PUT_vote(self):
        self._create_vote(content={
                    'content_type': '9',
                    'object_id':'1',
                    'vote':UPVOTE,
                    },
                    user='user1',
                    password='user1')
        #Update the annotation    
        vote = Vote.objects.all()[0]
        #Try changing the vote.
        string_data = {
                    'content_type': '9',
                    'object_id':'1',
                    'vote':UPVOTE,
                    }
        json_data = json.dumps(string_data)
        url = '/voting/votes/'+ str(vote.id)+'/'
        response = self.client.put(
            url,
            content_type='application/json',
            data = json_data,
         )
        
        #print "Response"
        #print response.content.decode()       
        self.assertEqual(Vote.objects.all().count(), 1)
        annotation = Vote.objects.all()[0]
        #print 'Annotation content_object'
        #print annotation.content_object
    
    def test_vote_on_own_post(self):
        self.client.logout()
        self.client.force_authenticate(user=self.author)
        self._require_login('craft','craft')
        string_data = {
                    'content_type': '9',
                    'object_id':'1',
                    'vote':'1',
                    }
        json_data = json.dumps(string_data)
        response =  self.client.post(
            '/voting/votes/',
            content_type='application/json',
            data = json_data,
         )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Status code does not match")
    
    def test_get_votes_by_user(self):
        pass
    
    def test_get_score(self):
        self._create_votes((UPVOTE, UPVOTE))
        
        vote = Vote.objects.get_score(self.article)
        
    def test_get_user_vote(self):
        pass
    
    def test_get_top_rated_posts(self):
        pass
    
    def test_get_most_downvoted_posts(self):
        pass
    
    def test_get_blogcontent(self):
        self._create_vote(content={
                    'content_type': '9',
                    'object_id':'1',
                    'vote':UPVOTE,
                    },
                    user='user1',
                    password='user1')
        
        self.client.force_authenticate(user=self.user2)
        self._require_login('user2','user2')
        
        self._create_vote(content={
                    'content_type': '9',
                    'object_id':'1',
                    'vote':DOWNVOTE,
                    },
                    user='user2',
                    password='user2')
        self.client.force_authenticate(user=self.author)
        self._require_login('craft','craft')
        response = self.client.get('/voting/blogcontent/1/')
        
        print(response.content.decode())
       
    