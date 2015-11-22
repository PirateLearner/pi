from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
import datetime

from PirateLearner.models import BaseContentClass

class Messages(BaseContentClass):
    """
        Message Model
        basic element for thread, which is to be exchanged between users
    """
    sender = models.ForeignKey(User, related_name='message_sender')
    body = models.TextField(blank=False)
    parent = models.ForeignKey('self', null=True)
    created = models.DateTimeField(editable=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        return super(Messages, self).save(*args, **kwargs)


class Thread(BaseContentClass):
    """
        Thread Model
        Thread is collection of messages exchanges between users
    """
    participants = models.ManyToManyField(User, related_name='thread_participants')
    last_message = models.ForeignKey(Messages, related_name='last_message_in_thread', verbose_name='Last Message')
    messages = models.ManyToManyField(Messages, related_name='thread_messages', verbose_name='Thread Messages')
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        return super(Thread, self).save(*args, **kwargs)


class ParticipantThreads(BaseContentClass):
    """
        Participant Thread Model
        Has collection of threads for the participant
    """
    participant = models.ForeignKey(User, related_name='thread_participant', verbose_name='Thread Participant')
    threads = models.ManyToManyField(Thread, related_name='participant_threads', verbose_name='Participant Threads')

    class Meta:
        verbose_name = 'Participant Thread'
        verbose_name_plural = 'Participant Threads'


class ParticipantNotifications(BaseContentClass):
    """
        Participant Notification Model
        Notifications generated when a message is exchanged between users
    """
    participant = models.ForeignKey(User, related_name='notified_participant', verbose_name='Notification Participant')
    thread = models.ForeignKey(Thread, related_name='participant_thread')
    message_count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Participant Notification'
        verbose_name_plural = 'Participant Notifications'


def create_message(sender, body):
    return Messages.objects.create(sender=sender, body=body)


def get_thread_messages(thread_id, user, count=1):

    if Thread.objects.filter(participants=user).count():
        thread = Thread.objects.filter(pk=thread_id).get()
        return thread, thread.messages.all().order_by('created')
    else:
        return False, False


def get_thread(sender, receiver, last_msg):

    """
       return existing thread if exists b/w sender and receiver
       else
       create new thread and add participants and return it
    """
    thread = Thread.objects.filter(participants=sender).filter(participants=receiver)[0]
    created = False
    if not thread:
        thread = Thread.objects.create(last_message=last_msg)
        thread.participants.add(sender, receiver)
        created = True
    else:
        thread = thread.get()

    return thread, created


def get_user_threads(user):
    """
        returns all threads in which user has
        participated
    """
    thread = ParticipantThreads.objects.filter(participant=user)
    if thread:
        return thread.get().threads.all().order_by('-updated')
    else:
        return []


def add_thread(participant, thread):
    participant, created = ParticipantThreads.objects.get_or_create(participant=participant)
    participant.threads.add(thread)
    return created


def update_count(participant, thread):
    """
        updates message count for participant
    """
    ParticipantNotifications.objects.filter(
        participant=participant, thread=thread).update(message_count=0)


def get_user_notifications(user):
    """
        returns notifications for user
    """

    return ParticipantNotifications.objects.filter(participant=user, message_count__gt=0).order_by('-updated')


def get_notification_count(user):
    """
        returns user notification count
    """
    return get_user_notifications(user).count()


def create_notification(participant, thread):
    """
        creates notification for the user
    """
    notification, created = ParticipantNotifications.objects.get_or_create(participant=participant, thread=thread)
    notification.message_count += 1
    notification.save()