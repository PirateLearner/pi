"""
Signals relating to comments.
"""
from django.dispatch import Signal

# Sent just before a comment will be posted (after it's been approved and
# moderated; this can be used to modify the comment (in place) with posting
# details or other such actions. If any receiver returns False the comment will be
# discarded and a 400 response. This signal is sent at more or less
# the same time (just before, actually) as the Comment object's pre-save signal,
# except that the HTTP request is sent along with this signal.
annotation_will_be_posted = Signal(providing_args=["annotations", "request"])

# Sent just after a comment was posted. See above for how this differs
# from the Comment object's post-save signal.
annotation_was_posted = Signal(providing_args=["annotations", "request"])

# Sent after a comment was "flagged" in some way. Check the flag to see if this
# was a user requesting removal of a comment, a moderator approving/removing a
# comment, or some other custom user flag.
annotation_was_flagged = Signal(providing_args=["annotations", "flag", "created", "request"])