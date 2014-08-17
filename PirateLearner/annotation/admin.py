from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _, ungettext
from django.utils.html import escape, format_html

from annotation.models import Annotation
from annotation import get_model
from annotation.views.moderation import perform_flag, perform_approve, perform_delete


class UsernameSearch(object):
    """The User object may not be auth.User, so we need to provide
    a mechanism for issuing the equivalent of a .filter(user__username=...)
    search in CommentAdmin.
    """
    def __str__(self):
        return 'user__%s' % get_user_model().USERNAME_FIELD


class AnnotationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('object_link', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'body')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'paragraph_id', 'privacy', 'privacy_override_flag')}
        ),
     )

    list_display = ('name', 'content_type', 'object_link', 'submit_date')
    list_filter = ('submit_date', 'site')
    date_hierarchy = 'submit_date'
    readonly_fields = ('submit_date','object_link')
    ordering = ('-submit_date',)
    raw_id_fields = ('user',)
    search_fields = ('body', UsernameSearch())
    actions = ["approve_comments", "remove_comments"]


    def object_link(self, comment):
        object = comment.content_object
        title = unicode(object)
        return u'<a href="{0}">{1}</a>'.format(escape(object.get_absolute_url()), (title))
    
    object_link.short_description = _("Page")
    object_link.allow_tags = True

    def get_actions(self, request):
        actions = super(AnnotationAdmin, self).get_actions(request)
        # Only superusers should be able to delete the comments from the DB.
        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')
        if not request.user.has_perm('annotation.can_moderate'):
            if 'approve_comments' in actions:
                actions.pop('approve_comments')
            if 'remove_comments' in actions:
                actions.pop('remove_comments')
        return actions

    def flag_comments(self, request, queryset):
        self._bulk_flag(request, queryset, perform_flag,
                        lambda n: ungettext('flagged', 'flagged', n))
    flag_comments.short_description = _("Flag selected comments")

    def approve_comments(self, request, queryset):
        self._bulk_flag(request, queryset, perform_approve,
                        lambda n: ungettext('approved', 'approved', n))
    approve_comments.short_description = _("Approve selected comments")

    def remove_comments(self, request, queryset):
        self._bulk_flag(request, queryset, perform_delete,
                        lambda n: ungettext('removed', 'removed', n))
    remove_comments.short_description = _("Remove selected comments")

    def _bulk_flag(self, request, queryset, action, done_message):
        """
        Flag, approve, or remove some comments from an admin action. Actually
        calls the `action` argument to perform the heavy lifting.
        """
        n_comments = 0
        for comment in queryset:
            action(request, comment)
            n_comments += 1

        msg = ungettext('1 comment was successfully %(action)s.',
                        '%(count)s comments were successfully %(action)s.',
                        n_comments)
        self.message_user(request, msg % {'count': n_comments, 'action': done_message(n_comments)})

# Only register the default admin if the model is the built-in comment model
# (this won't be true if there's a custom comment app).
if get_model() is Annotation:
    admin.site.register(Annotation, AnnotationAdmin)