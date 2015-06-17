from __future__ import absolute_import

from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

import annotations
from annotation import signals
from annotation.views.utils import next_redirect, confirmation_view


from django.http import HttpResponse, HttpResponseBadRequest

import json
import sys

class AnnotationPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """
    def __init__(self, why):
        super(AnnotationPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("annotations/400-debug.html", {"why": why})


@csrf_protect
@require_POST
#There must be a require logged in clause here
def post_annotation(request, next=None, using=None):
    """
    Post an annotations.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.get_username()
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return AnnotationPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        return AnnotationPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return AnnotationPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return AnnotationPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError) as e:
        return AnnotationPostBadRequest(
            "Attempting go get content-type %r and object PK %r exists raised %s" % \
                (escape(ctype), escape(object_pk), e.__class__.__name__))


    # Construct the comment form
    #target contains the object for content_type with which the annotation is associated
    #data is the comment
    form = annotations.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return AnnotationPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    # If there are errors
    if form.errors:
        template_list = [
            # Now the usual directory based template hierarchy.
            "annotations/%s/%s/preview.html" % (model._meta.app_label, model._meta.module_name),
            "annotations/%s/preview.html" % model._meta.app_label,
            "annotations/preview.html",
        ]
        return render_to_response(
            template_list, {
                "body": form.data.get("body", ""),
                "form": form,
                "next": data.get("next", next),
            },
            RequestContext(request, {})
        )

    # Otherwise create the comment
    # To create an annotations, the user must be logged in, thus that field must
    # be specified while getting an object
    #Or maybe we could create an object and assign it later. But lets not enforce it
    #here.
    
    comment = form.get_comment_object(request)
    
    if request.user.is_authenticated():
        comment.user = request.user
    

    # Signal that the comment is about to be saved
    responses = signals.annotation_will_be_posted.send(
        sender=comment.__class__,
        annotations=comment,
        request=request
    )

    for (receiver, response) in responses:
        if response == False:
            return AnnotationPostBadRequest(
                "annotation_will_be_posted receiver %r killed the comment" % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.annotation_was_posted.send(
        sender=comment.__class__,
        annotations=comment,
        request=request
    )

    return next_redirect(request, fallback=next or 'annotations:annotations-comment-done',
        c=comment._get_pk_val())



@csrf_protect
@require_POST
def post_annotation_ajax(request, using=None):
    """
    Post an annotations, via an Ajax call.
    Note: This is an experimental code. This must be replaced by the Tastypie implementation
    """
    if not request.is_ajax():
        return HttpResponseBadRequest("Expecting Ajax call")

    # This is copied from django.contrib.comments.
    # Basically that view does too much, and doesn't offer a hook to change the rendering.
    # The request object is not passed to next_redirect for example.
    #
    # This is a separate view to integrate both features. Previously this used django-ajaxcomments
    # which is unfortunately not thread-safe (it it changes the comment view per request).


    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.username
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return AnnotationPostBadRequest("Missing content_type or object_pk field.")
    try:
        object_pk = long(object_pk)
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except ValueError:
        return AnnotationPostBadRequest("Invalid object_pk value: {0}".format(escape(object_pk)))
    except TypeError:
        return AnnotationPostBadRequest("Invalid content_type value: {0}".format(escape(ctype)))
    except AttributeError:
        return AnnotationPostBadRequest("The given content-type {0} does not resolve to a valid model.".format(escape(ctype)))
    except ObjectDoesNotExist:
        return AnnotationPostBadRequest("No object matching content-type {0} and object PK {1} exists.".format(escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError) as e:
        return AnnotationPostBadRequest("Attempting go get content-type {0!r} and object PK {1!r} exists raised {2}".format(escape(ctype), escape(object_pk), e.__class__.__name__))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = annotations.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return AnnotationPostBadRequest("The comment form failed security verification: {0}".format)

    # If there are errors or if we requested a preview show the comment
    if preview:
        comment = form.get_comment_object(request) if not form.errors else None
        return _ajax_result(request, form, "preview", comment, object_id=object_pk)
    if form.errors:
        return _ajax_result(request, form, "post", object_id=object_pk)


    # Otherwise create the comment
    comment = form.get_comment_object(request)
    if request.user.is_authenticated():
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.annotation_will_be_posted.send(
        sender  = comment.__class__,
        annotations = comment,
        request = request
    )

    for (receiver, response) in responses:
        if response is False:
            return AnnotationPostBadRequest("annotation_will_be_posted receiver {0} killed the comment".format(receiver.__name__))

    # Save the comment and signal that it was saved
    comment.save()
    signals.annotation_was_posted.send(
        sender  = comment.__class__,
        annotations = comment,
        request = request
    )

    return _ajax_result(request, form, "post", comment, object_id=object_pk)


def _ajax_result(request, form, action, comment=None, object_id=None):
    # Based on django-ajaxcomments, BSD licensed.
    # Copyright (c) 2009 Brandon Konkle and individual contributors.
    #
    # This code was extracted out of django-ajaxcomments because
    # django-ajaxcomments is not threadsafe, and it was refactored afterwards.

    success = True
    json_errors = {}

    if form.errors:
        for field_name in form.errors:
            field = form[field_name]
            json_errors[field_name] = _render_errors(field)
        success = False

    json_return = {
        'success': success,
        'action': action,
        'errors': json_errors,
        'object_id': object_id,
    }

    if comment is not None:
        context = {
            'annotations': comment,
            'action': action,
            'preview': (action == 'preview'),
        }
        comment_html = render_to_string('annotations/annotations.html', context, context_instance=RequestContext(request))

        json_return.update({
            'html': comment_html,
            'comment_id': comment.id,
            'parent_id': None,
        })

    json_response = json.dumps(json_return)
    return HttpResponse(json_response, content_type="application/json")


def _render_errors(field):
    """
    Render form errors in crispy-forms style.
    """
    template = '{0}/layout/field_errors.html'.format(appsettings.CRISPY_TEMPLATE_PACK)
    return render_to_string(template, {
        'field': field,
        'form_show_errors': True,
    })

annotation_done = confirmation_view(
    template="annotations/posted.html",
    doc="""Display a "annotations was posted" success page."""
)