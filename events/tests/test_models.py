import base64

from django.core import mail
from django.utils.six.moves import cPickle as pickle
from django.test import TestCase
from django.test.utils import override_settings

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from ..conf import settings
from ..models import EventType, EventQueueBatch, EventFilter
from ..models import send, queue


from . import get_backend_id


class BaseTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("Anshul", "anshulthakurjourneyendless@gmail.com", "123456")
        self.user2 = get_user_model().objects.create_user("Abhishek", "abnith.rai812@gmail.com", "123456")
        EventType.create("label", "display", "description")
        self.event_type = EventType.objects.get(label="label")

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.event_type.delete()


class TestEventType(TestCase):

    def test_create(self):
        label = "friends_invite"
        EventType.create(label, "Invitation Received", "you received an invitation",
                          verbosity=2)
        n = EventType.objects.get(label=label)
        self.assertEqual(str(n), label)
        # update
        EventType.create(label, "Invitation for you", "you got an invitation", 
                          verbosity=2)
        n = EventType.objects.get(pk=n.pk)
        self.assertEqual(n.display, "Invitation for you")
        self.assertEqual(n.description, "you got an invitation")


class TestEventFilter(BaseTest):
    def test_for_user(self):
        email_id = get_backend_id("email")
        notice_setting = EventFilter.objects.create(
            user=self.user,
            event_type=self.event_type,
            action=email_id
        )
        self.assertEqual(
            EventFilter.for_user(self.user, self.event_type, email_id, scoping=None),
            notice_setting
        )


class TestProcedures(BaseTest):
    def setUp(self):
        super(TestProcedures, self).setUp()
        mail.outbox = []

    def tearDown(self):
        super(TestProcedures, self).tearDown()
        EventQueueBatch.objects.all().delete()

    @override_settings(SITE_ID=1)
    def test_send_text(self):
        Site.objects.create(domain="localhost", name="localhost")
        users = [self.user, self.user2]
        send(users, "label")
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(self.user.email, mail.outbox[0].to)
        self.assertIn(self.user2.email, mail.outbox[1].to)

    @override_settings(SITE_ID=1)
    def test_send_html(self):
        Site.objects.create(domain="localhost", name="localhost")
        users = [self.user, self.user2]
        send(users, "label",extra_context= {"Message": "Hey There!!"}, html=True)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(self.user.email, mail.outbox[0].to)
        self.assertIn(self.user2.email, mail.outbox[1].to)
    

    @override_settings(SITE_ID=1)
    def test_queue(self):    
        users = [self.user, self.user2]
        queue(users, "label")
        self.assertEqual(EventQueueBatch.objects.count(), 1)
        batch = EventQueueBatch.objects.all()[0]
        notices = pickle.loads(base64.b64decode(batch.pickled_data))
        self.assertEqual(len(notices), 2)



    @override_settings(SITE_ID=1)
    def test_queue_queryset(self):
        users = get_user_model().objects.all()
        queue(users, "label")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(EventQueueBatch.objects.count(), 1)
