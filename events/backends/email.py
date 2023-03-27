from events.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.translation import gettext_lazy as ugettext
from django.utils.html import strip_tags

from events.backends.base import BaseBackend


class EmailBackend(BaseBackend):
    spam_sensitivity = 2

    def can_send(self, user, notice_type, scoping):
        can_send = super(EmailBackend, self).can_send(user, notice_type, scoping)
        if can_send and user.email:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, **kwargs):
        """
        INPUT:  recipient --> User instance
                sender --> User instance if not None
                notice_type --> Instace of EventType
                extra_context --> named argument
                html --> named argument can be True or False
                template_name --> named argument Name of template if html is True. If None in case of html=True then
                                default template would be used.
        """

        context = self.default_context()
        if sender is None:
            sender = settings.DEFAULT_FROM_EMAIL
        else:
            sender = sender.email

        extra_context = kwargs.get('extra_context',None)

        context.update({
            "recipient": recipient,
            "sender": sender,
        })
        if extra_context:
            notice = extra_context.get('notice',None)
            if notice is None:
                extra_context['notice'] = ugettext(notice_type.display)
            context.update(extra_context)

        messages = self.get_formatted_messages((
            "short.txt",
            "full.txt"
        ), notice_type.label, context)

        subject = extra_context.get('subject',None)
        if subject is None:
            subject = "".join(render_to_string("events/notifications/email_subject.txt", {
                "message": messages["short.txt"],
            }, context).splitlines())

        html = kwargs.get('html',False)
        ## check if it is html message or not
        if html:
            template = get_template(kwargs.get('template_name',"events/notifications/default.html"))
            html_part = template.render(context)
            text_part = strip_tags(html_part)
            files = kwargs.get('files', None)

            msg = EmailMultiAlternatives(subject,
                                        text_part,
                                        sender,
                                        [recipient.email])
            msg.attach_alternative(html_part, "text/html")

            if files:
                if type(files) != list:
                    files = [files,]

                for file in files:
                    msg.attach_file(file)
            print(("Sending html mail to ", recipient.email, " sender ", sender        ))
            return msg.send(fail_silently = True)

        else:

            body = render_to_string("events/notifications/email_body.txt", {
                "message": messages["full.txt"],
            }, context)
            print(("Sending text mail to ", recipient.email, " sender ", sender))
            return send_mail(subject, body, sender, [recipient.email])
