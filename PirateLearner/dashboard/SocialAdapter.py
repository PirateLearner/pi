from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        print("LOGS: pre_social_login called ")
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            print("LOGS: Social Account already Exist return!!!")
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            print("LOGS: Email not found in Social Account return!!!")
            return

        email = sociallogin.account.extra_data['email'].lower()
        print("LOGS: Email found in Social Account ", email)


        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email_address = EmailAddress.objects.get(email__iexact=email)
            print("LOGS: Email found in Social Account Accessing the existing Email address")
            # if it does, connect this new social login to the existing user
            user = email_address.user
            print("LOGS: Connecting user")
            sociallogin.connect(request, user)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            # above method does not work if same email is used in local login and there is no entry in EmailAddress model of AllAuth
            # so checking for the user account
            try:
                user = User.objects.get(email__iexact=email)
                print("LOGS: E-mail found in User Account")
                # if it does, connect this new social login to the existing user
                print("LOGS: Connecting user")
                sociallogin.connect(request, user)

            # if it does not, let allauth take care of this new social account
            except User.DoesNotExist:
                return
    def is_open_for_signup(self, request, sociallogin):
        # To disable social account signup, return False. Otherwise return True(Default).
        return True

