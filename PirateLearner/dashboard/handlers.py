from events.decorators import register_handle
from events.models import send
from django.contrib.contenttypes.models import ContentType

@register_handle("user_signed_up")
def handle_submit_event(sender, *args,**kwargs):
    """
    On sign-up event send the Mail to Group Administrator and welcome mail to user
    """

    user = kwargs.get("user",None)
    label = kwargs.get("event_label",None)
    source_content_type = kwargs.get("source_content_type",None)
    source_object_id = kwargs.get("source_object_id",None)

    if label is None:
        label = args[0]

    if user is None:
        user = args[1]

    if source_content_type is None:
        source_content_type = args[2]

    if source_object_id is None:
        source_object_id = args[3]

    # get object from content type
    obj = source_content_type.get_object_for_this_type(pk=source_object_id)

    ## send the welcome mail
    extra_context = { "subject": "Welcome to PirateLearner!"}
    template_name = "events/notifications/{0}/welcome.html".format(label)

    ret  = send([user],label,extra_context = extra_context, html=True, template_name=template_name)
    print("Send to user return ", ret)

    extra_context = { "subject": "User signed-up!!!", "user": obj}
    template_name = "events/notifications/{0}/admin.html".format(label)
    ret  = send("Administrator",label,extra_context = extra_context, html=True, template_name=template_name)
    print("Send to Admistrator return ", ret)


