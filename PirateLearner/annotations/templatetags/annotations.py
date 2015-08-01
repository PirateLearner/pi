from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text

import annotations

from django.conf import settings
from django.template import Node
from django.core import context_processors
from django.template.loader import get_template
from annotations.models import get_annotation_for_model

register = template.Library()


@register.inclusion_tag("annotations/templatetags/ajax_annotation_tags.html", takes_context=True)
def ajax_annotation_tags(context, for_, target_object):
    """
    Display the required ``<div>`` elements to let the Ajax comment functionality work with your form.
    """
    new_context = {
        'STATIC_URL': context.get('STATIC_URL', None),
        'target_object': target_object,
    }

    # Be configuration independent:
    if new_context['STATIC_URL'] is None:
        try:
            request = context['request']
        except KeyError:
            new_context.update({'STATIC_URL': settings.STATIC_URL})
        else:
            new_context.update(context_processors.static(request))

    return new_context


@register.filter
def annotation_count(content_object):
    """
    Return the number of annotations posted at a target object.

    You can use this instead of the ``{% get_annotation_count for [object] as [varname]  %}`` tag.
    """
    return get_annotation_for_model(content_object).count()


class AnnotationList(Node):
    def render(self, context):
        # Include proper template, avoid parsing it twice by operating like @register.inclusion_tag()
        if not getattr(self, 'nodelist', None):
            template = get_template("annotations/templatetags/flat_list.html")
            self.nodelist = template

        # NOTE NOTE NOTE
        # HACK: Determine the parent object based on the comment list queryset.
        # the {% render_comment_list for article %} tag does not pass the object in a general form to the template.
        # Not assuming that 'object.pk' holds the correct value.
        #
        # This obviously doesn't work when the list is empty.
        # To address that, the client-side code also fixes that, by looking for the object ID in the nearby form.
        target_object_id = context.get('target_object_id', None)
        if not target_object_id:
            comment_list = context['annotation_list']
            if isinstance(comment_list, list) and comment_list:
                target_object_id = comment_list[0].object_pk

        # Render the node
        context['target_object_id'] = target_object_id
        return self.nodelist.render(context)


@register.tag
def annotation_list(parser, token):
    """
    A tag to select the proper template for the current comments app.
    """
    return AnnotationList()


class BaseAnnotationNode(template.Node):
    """
    Base helper class (abstract) for handling the get_annotation_* template tags.
    Looks a bit strange, but the subclasses below should make this a bit more
    obvious.
    
    There can be 5 or 6 tokens in a statement.
    
    <method> for <content_object>     as  <name>
    0        1            2            3    4        5    
    <method> for <content_type_id> <object_pk> as <name>
    0        1        2                3        4    5
    """

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse get_annotation_list/count/form and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for obj as varname %}
        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            #Return the object class as object expression and friendly alias as as_varname
            return cls(
                #compile_filter returns a tuple of variable and it's filters, which were passed in as a complete string
                object_expr = parser.compile_filter(tokens[2]),
                as_varname = tokens[4],
            )

        # {% get_whatever for app.model pk as varname %}
        elif len(tokens) == 6:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                ctype = BaseAnnotationNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr = parser.compile_filter(tokens[3]),
                as_varname = tokens[5]
            )

        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])

    @staticmethod
    def lookup_content_type(token, tagname):
        try:
            app, model = token.split('.')
            return ContentType.objects.get_by_natural_key(app, model)
        except ValueError:
            raise template.TemplateSyntaxError("Third argument in %r must be in the format 'app.model'" % tagname)
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError("%r tag has non-existant content-type: '%s.%s'" % (tagname, app, model))

    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, body=None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError("Annotation nodes must be given either a literal object or a ctype and object pk.")
        self.comment_model = annotations.get_model()
        self.as_varname = as_varname
        self.ctype = ctype
        self.object_pk_expr = object_pk_expr
        self.object_expr = object_expr
        self.body = body

    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ''

    def get_query_set(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.comment_model.objects.none()

        qs = self.comment_model.objects.filter(
            content_type = ctype,
            object_pk    = smart_text(object_pk),
            site__pk     = settings.SITE_ID,
        )

        # The is_public and is_removed fields are implementation details of the
        # built-in comment model's spam filtering system, so they might not
        # be present on a custom comment model subclass. If they exist, we
        # should filter on them.
        field_names = [f.name for f in self.comment_model._meta.fields]
        if 'is_public' in field_names:
            qs = qs.filter(is_public=True)
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(is_removed=False)

        return qs

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                #If object name was passed, then try to get an object instance from the context
                #This will return an object with its keys
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            #If object and primary key were passed, then we just need to find the object_pk value
            return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        raise NotImplementedError

class AnnotationListNode(BaseAnnotationNode):
    """Insert a list of annotations into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return list(qs)

class AnnotationCountNode(BaseAnnotationNode):
    """Insert a count of annotations into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return qs.count()

class AnnotationFormNode(BaseAnnotationNode):
    """Insert a form for the comment model into the context."""

    def get_form(self, context):
        obj = self.get_object(context)
        if obj:
            return annotations.get_form()(obj)
        else:
            return None

    def get_object(self, context):
        if self.object_expr:
            try:
                return self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None
        else:
            object_pk = self.object_pk_expr.resolve(context,
                    ignore_failures=True)
            return self.ctype.get_object_for_this_type(pk=object_pk)

    def render(self, context):
        context[self.as_varname] = self.get_form(context)
        return ''

class RenderAnnotationFormNode(AnnotationFormNode):
    """Render the annotations form directly"""

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_annotation_form and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% render_comment_form for obj %}
        if len(tokens) == 3:
            return cls(object_expr=parser.compile_filter(tokens[2]))

        # {% render_comment_form for app.models pk %}
        elif len(tokens) == 4:
            return cls(
                ctype = BaseAnnotationNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr = parser.compile_filter(tokens[3])
            )

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            template_search_list = [
                "annotations/%s/%s/form.html" % (ctype.app_label, ctype.model),
                "annotations/%s/form.html" % ctype.app_label,
                "annotations/form.html"
            ]
            context.push()
            formstr = render_to_string(template_search_list, {"form" : self.get_form(context)}, context)
            context.pop()
            return formstr
        else:
            return ''

class RenderAnnotationListNode(AnnotationListNode):
    """Render the annotations list directly"""

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_list and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% render_comment_list for obj %}
        if len(tokens) == 3:
            return cls(object_expr=parser.compile_filter(tokens[2]))

        # {% render_comment_list for app.models pk %}
        elif len(tokens) == 4:
            return cls(
                ctype = BaseAnnotationNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr = parser.compile_filter(tokens[3])
            )

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            template_search_list = [
                "annotations/%s/%s/list.html" % (ctype.app_label, ctype.model),
                "annotations/%s/list.html" % ctype.app_label,
                "annotations/list.html"
            ]
            qs = self.get_query_set(context)
            context.push()
            liststr = render_to_string(template_search_list, {
                "annotation_list" : self.get_context_value_from_queryset(context, qs)
            }, context)
            context.pop()
            return liststr
        else:
            return ''

# We could just register each classmethod directly, but then we'd lose out on
# the automagic docstrings-into-admin-docs tricks. So each node gets a cute
# wrapper function that just exists to hold the docstring.

@register.tag
def get_annotation_count(parser, token):
    """
    Gets the annotations count for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_annotation_count for [object] as [varname]  %}
        {% get_annotation_count for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_annotation_count for event as annotation_count %}
        {% get_annotation_count for calendar.event event.id as annotation_count %}
        {% get_annotation_count for calendar.event 17 as annotation_count %}

    """
    return AnnotationCountNode.handle_token(parser, token)

@register.tag
def get_annotation_list(parser, token):
    """
    Gets the list of annotations for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_annotation_list for [object] as [varname]  %}
        {% get_annotation_list for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_annotation_list for event as annotation_list %}
        {% for annotations in annotation_list %}
            ...
        {% endfor %}

    """
    return AnnotationListNode.handle_token(parser, token)

@register.tag
def render_annotation_list(parser, token):
    """
    Render the annotations list (as returned by ``{% get_annotation_list %}``)
    through the ``annotations/list.html`` template

    Syntax::

        {% render_annotation_list for [object] %}
        {% render_annotation_list for [app].[model] [object_id] %}

    Example usage::

        {% render_annotation_list for event %}

    """
    return RenderAnnotationListNode.handle_token(parser, token)

@register.tag
def get_annotation_form(parser, token):
    """
    Get a (new) form object to post a new comment.

    Syntax::

        {% get_annotation_form for [object] as [varname] %}
        {% get_annotation_form for [app].[model] [object_id] as [varname] %}
    """
    return AnnotationFormNode.handle_token(parser, token)

@register.tag
def render_annotation_form(parser, token):
    """
    Render the annotations form (as returned by ``{% render_annotation_form %}``) through
    the ``annotations/form.html`` template.

    Syntax::

        {% render_annotation_form for [object] %}
        {% render_annotation_form for [app].[model] [object_id] %}
    """
    return RenderAnnotationFormNode.handle_token(parser, token)

@register.simple_tag
def annotation_form_target():
    """
    Get the target URL for the annotations form.

    Example::

        <form action="{% annotation_form_target %}" method="post">
    """
    return annotations.get_form_target()

@register.simple_tag
def get_annotation_permalink(comment, anchor_pattern=None):
    """
    Get the permalink for an annotations, optionally specifying the format of the
    named anchor to be appended to the end of the URL.

    Example::
        {% get_annotation_permalink annotations "#c%(id)s-by-%(user_name)s" %}
    """

    if anchor_pattern:
        return comment.get_absolute_url(anchor_pattern)
    return comment.get_absolute_url()
