from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import messages as mm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotAllowed, Http404
from .models import *
from .forms import MessageForm, ReplyForm


def home(request):
    """
        displays user specific threads
    """
    threads = get_user_threads(user=request.user)
    context = {
        'threads': threads
    }
    return render(request, 'home.html', context)


def save_message(request):
    """
        save new message
        create new thread if no thread exits between participants
            add message to thread
            add last message
            add participants
        create notifications for receiver
        add thread to each participant's thread set
    """
    form = MessageForm(request.user,request.POST)
    if form.is_valid():
        sender = request.user
        receiver = get_object_or_404(User, pk=request.POST['to'])
        msg = request.POST['body']
        # create message
        message = create_message(sender=sender, body=msg)
        # get or create thread
        thread, created = get_thread(sender=sender, receiver=receiver, last_msg=message)
        # update message parent if thread already exists
        # if not created:
        #     message.parent = thread.last_message
        #     message.save()
        thread.last_message = message
        thread.save()
        thread.messages.add(message)
        # assign this thread to participant 1
        add_thread(sender, thread)
        # assign this thread to participant 2
        add_thread(receiver, thread)

        # create notification regarding this message for receiver
        create_notification(participant=receiver, thread=thread)
        return True
    else:
        return False


def thread_messages(request, thread_id):
    thread, messages = get_thread_messages(thread_id=thread_id, user=request.user)
    if thread:
        update_count(participant=request.user, thread=thread)
        if request.method == 'POST':
            reply = ReplyForm(request.POST)
            if reply.is_valid():
                sender = request.user
                body = request.POST['body']
                message = create_message(sender=sender, body=body)
                message.parent = thread.last_message
                message.save()
                thread.messages.add(message)
                thread.last_message = message
                thread.save()
                participants = thread.participants.all()
                for participant in participants:
                    if participant != sender:
                        create_notification(participant=participant, thread=thread)
        form = ReplyForm()
        context = {
            'chats': messages,
            'form': form,
            'thread': thread
        }
        return render(request, 'thread_messages.html', context)
    else:
        return Http404()


def new_message(request):
    if request.method == 'POST':
        save_message(request)
    dest = request.GET.get('to',None)
    
    if dest:
        dest = User.objects.get(pk=dest)
        form = MessageForm(dest)
    else:
        form = MessageForm(request.user)
    context = {
        'form': form
    }
    return render(request,'new_message.html', context)