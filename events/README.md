# Event Handler App

`Event Handler App` is useful for sending the notifications to user for any specific event and perform any action by applying the hooks on the events. This App uses the same models and utility function structures as defined in the `pinax-notifications` App, and at the same time implement the event hooks so that other app can register for the events that have been created in the system, irrespective of its origin. We are using the `pinax-notifications` app for defining the Events and filters but we don't restrict the user to use the in-built actions. This App provides the means to register for the event and take any actions, whenever the event occurs; thus decoupling the actions from events. Though we do provide one default action named [send_html_email](# send-html-email) and other Apps can use it to send html mails for the corresponding events.

## Models

* ### EventType <a id="event-type"></a>

 EventType Model contains three fields named: `label`, `display`, and `discription`. Unlike `pinax-notifications` we don't have the default field as we believe that each event is elligible for any actions and event specific operations will be supported via hooks on that events. As this is an `Event Handler App` we have decoupled the delivery mechenism and we rely upon the App user to do whatever necessary on the reception of particular event.

* ### EventFilter

 This model represents the deny filters applied on the events for mail delivery system. It contains following fields:
 * user : Foreign Key to User Model.
 * notice_type :  Foreign Key to [EventType](#event-type) Model.
 * action :
 * scoping_content_type : Foriegn Key to ContentType used for Generic foreign key. (null=True, blank=True)
 * scoping_object_id: Positive Interger field used for Generic foreign key. (null=True, blank=True)
 * scoping: Generic Foriegn key used for linking the filters to specific object.

 By default there would be no filters, so every events are allowed to send notifications via [send_html_email](#send-html-email) to the users. Users can unsubscribe the events, by the use of views provided by the App. Other Apps may use this model for checking the elligibility of actions in their event hooks or they may create similar models if they need the filters at action level granularity.

* ### NoticeQueueBatch

 As `pinax-notifications` documentaion stated "_A queued notice. Denormalized data for a notice._" This model provides the means to store the notices for later use. In this way, another application, which is outside the web server, can retrieve these notices and perform the action accordingly thus reducing the load on web server. An management command ```send_bulk_mail``` is provided, which reads these notices and send email notifications to concerned users to demonstrate the procedure. A utility function have been provided to store notice in the model named : ```queue(users, label, extra_context=None, sender=None, template=None):```

## urls and views

EventFilter url and corresponding view have been provided to configure the deny filters of mail notifications for all the events available in the Database. These filters are user specific so only logged in users can view this page.

## <a name="Signals"></a>Signals

This App defines and listen on a signal named `generate_event`,  which should be sent by the App whenever they want to generate the Event. Following arguments should be available in the signal:

 * event_label : label that corresponds to an event which is generated. It must belongs to one of the instace of [EventType](#event-type) Model.
 * source_content_type: ContentType of source that generated the event. (May be None)
 * source_object_id: Object id of source that generated the event. (May be None)
 * user: current logged in user instace. (May be None)

## Event Hooks

A decorator `event_trigger` has been provided for registration of functions. Different App can register on the same Event and perform their specific actions or use [send_html_email](#send-html-email) for sending notification to user. Decorator don't check for duplicity of actions and runs all the functions registered for that event and there is no sequence, so it is the responsibility of developer to ensure that two functions which are performing same action or are interrelated, are not registered with the `event_trigger`. `event_trigger` takes one arguments named label. This label should belong to one of the [EventType](#event-type) stored in the Database; if not it will raise the `InvalidEvent` exception. Function registering via `event_trigger` should have following signatures:
```python
@event_trigger("event_label")
def function(*args, **kwargs):
        pass
```
or
```python
@event_trigger("event_label")
def function(label,user, **kwargs):
        pass
```

The above function must parse the `args` and `kwargs` for arguments defined in [signal section](# Signals). Functions register for event handling via the `event_trigger` decorator should be imported during initialization phase of your App. To do that these functions may be defined in `__init__.py` or the files they are defined in may be imported in `__init__.py`. e.g. Reason for this strategy is that `__init__.py` of each App listed in `INSTALLED_APP` is imported at start-up.
```python
# __init__.py

@event_trigger("event_label")
def function(label,user, **kwargs):
        pass
```
or

```python
#__init__.py
import handlers

#handlers.py
@event_trigger("event_label")
def function(label,user, **kwargs):
        pass
```

## Utility functions

* ```send_html_email(to, label, extra_context=None, sender=None, template=None)```: <a id="send-html-email"></a>

 send email to users for Event identified by label. extra_context can be passed which would be used in rendering the given template. If template is `None` then `event_handlers/default.html` would be used. `to` is interpreted in two ways; first if it is list then it represent the users list for which mail have to be sent; second if it's str object then it represent the group name. In second case mail is sent to all the users that belong to the given group.
* ```queue(users, label, extra_context=None, sender=None, template=None)```:

 Store the event in `NoticeQueueBatch` for further processing by another application.
* ```check_filter(cls, user, notice_type, scoping)```:

  This class Method is defined in Model `EventFilter` and can be used to check for deny filter of given user and Event and scope.
* ```create(cls, label, display, description, verbosity=1)```:

   This class Method is defined in Model [EventType](#event-type) and can be used by other App to create the Events. verbosity can be used to open the debug prints.
* ```send_all(**kwargs)```:
 Process all the Notices that are stored in the Model `NoticeQueueBatch` and send email notifications to corresponding users if no deny filter is found. This method serves as an example to process all the notices and perform action on them. This function will check for `notice_delete` flag in kwargs and will delete all the notices if true.

## Config Settings

 * DEFAULT_HTTP_PROTOCOL: use to append http/https before urls in mails.
 * DEFAULT_FROM_EMAIL: Default sender email address.
