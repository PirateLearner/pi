
from django.urls import path, re_path, include
from .views import *

app_name="pl_messages"

urlpatterns = [
    path('', home, name='home_message'),
    path('compose/', new_message, name='new_message'),
    path('all/', home, name='all_threads'),
    path('save/', save_message, name='save_message'),
    re_path(r'^thread/view/([0-9]+)$', thread_messages, name='thread_messages'),

]
