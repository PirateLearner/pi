# Create your views here.
from django.dispatch import receiver
from django.template import RequestContext, loader
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.contrib.auth.decorators import login_required
from dashboard.models import UserProfile
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from dashboard.forms import ProfileEditForm
#from allauth.account.models import EmailAccount
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from taggit.models import Tag
from allauth.account.views import LoginView
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount

from django.contrib.auth.signals import user_logged_in

# import from blogging 
from blogging.models import get_published_count, get_pending_count, get_draft_count, get_contribution_count 
# import from bookmarks
from bookmarks.models import get_bookmarks_count
# import from annotaions
from annotations.models import get_annotations_count 
# import from Voting
from voting.models import Vote
# import from pl_messages
from pl_messages.models import get_notification_count, get_user_notifications


@receiver(user_logged_in)
def CreateProfile(sender, request, user,**kwargs):
    """
    This function catches the signal for social login or social account add and check for the User profile object: if exist then do nothing,
    if not then create it and set the gender field.
    """
    try:
        
        profile = UserProfile.objects.get(user = user)
        print "LOGS: User profile exist do nothing"
    except UserProfile.DoesNotExist:
        print "LOGS: User profile does not exist"
  
        profile = UserProfile()
        profile.user = user
        try:
            sociallogin = SocialAccount.objects.get(user=user)
            print "LOGS: Caught the signal--> Printing extra data of the account: \n", sociallogin.extra_data
            if('google' == sociallogin.provider ):
                user.first_name = sociallogin.extra_data['given_name']
                user.last_name = sociallogin.extra_data['family_name']
                user.save()
            elif ('facebook' == sociallogin.provider ):
                user.first_name = sociallogin.extra_data['first_name']
                user.last_name = sociallogin.extra_data['last_name']
                user.save()
            profile.gender = sociallogin.extra_data['gender']
        except:
            print "LOGS: Gender does not exist in social account"
        profile.save()
              

    
@login_required
def dashboard_home(request):
    template = loader.get_template('dashboard/home.html')
    profile = UserProfile.objects.get(user=request.user.id) or None
    # acquire all the statistics of User
    # Number of articles contributed, published, pending, drafted. 
    # Total number of comments, votes and annotations
    # Number of bookmarks
    stats = {}
    stats['article_total'] = get_contribution_count(request.user)
    stats['article_published'] = get_published_count(request.user)
    stats['article_draft'] = get_draft_count(request.user)
    stats['article_pending'] = get_pending_count(request.user)
    stats['bookmark_count'] = get_bookmarks_count(request.user);
    stats['annotations_count'] = get_annotations_count(request.user)
    stats['voting_count'] = Vote.objects.get_for_user_in_bulk(request.user).count()
    stats['notification_count'] = get_notification_count(request.user)
    context = RequestContext(request, {
                                       "profile":profile,"stats":stats,
                                      })
    return HttpResponse(template.render(context))

@login_required
def dashboard_profile(request,user_id):
    print "LOGS: DashBoard Profile called with user id " , user_id
    
    print "LOGS: User in request is ", request.user.id
    
    try:
        user_id = int(user_id)
        if request.user.id == user_id:
            return my_profile(request)
        else:
            return public_profile(request,user_id)
    except ValueError:
        print "LOGS:invalid request for user_id ", user_id
        raise Http404
    


def my_profile(request):
    template = loader.get_template('dashboard/profile.html')
    profile = UserProfile.objects.get(user=request.user.id)
    
    data = {
            'address': profile.address,
            'occupation' : profile.occupation,
            'website': profile.website,
            'interest': profile.interest.all(),
            'date_of_birth': profile.date_of_birth,
            }
    
    form = ProfileEditForm(initial = data)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        
        if form.is_valid():
            #form.save()
            print "printing form data", form.cleaned_data['address'] , form.cleaned_data['interest']
            print "LOGS: Profile form is Valid "
            try:
                profile = UserProfile.objects.get(user=request.user)
                profile.address = form.cleaned_data['address']
                profile.date_of_birth = form.cleaned_data['date_of_birth']
                profile.occupation = form.cleaned_data['occupation']
                profile.website = form.cleaned_data['website']
                profile.interest.set(*form.cleaned_data['interest'])
                profile.save()
                profile = UserProfile.objects.get(user=request.user)
                print "Printing interest after save ", profile.interest
                return HttpResponseRedirect(reverse('dashboard:dashboard-profile',kwargs = { 'user_id': int(profile.user.id) }))
            except User.DoesNotExist:
                raise Http404
        else:
            context = RequestContext(request, {
                                       'profile': profile,
                                       'profile_form': form,
                                      })
    else:
        context = RequestContext(request, {
                                       'profile': profile,
                                       'profile_form': form,
                                      })
    return HttpResponse(template.render(context))
    
def public_profile(request,user_id):
    
    try:
        user = User.objects.get(pk=user_id)
        profile = UserProfile.objects.get(user=user) or None
        template = loader.get_template('dashboard/public_profile.html')
        context = RequestContext(request, {
                                           'profile':profile
                                      })
        return HttpResponse(template.render(context))
    
    except User.DoesNotExist:
        raise Http404
    
@login_required
def manage_articles(request):
    template = loader.get_template('dashboard/manage.html')
    profile = UserProfile.objects.get(user=request.user.id) or None
    
    context = RequestContext(request, {
                                       "profile":profile,
                                      })
    return HttpResponse(template.render(context))

@login_required
def published_articles(request):
    template = loader.get_template('dashboard/published.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

@login_required
def pending_articles(request):
    template = loader.get_template('dashboard/pending.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

@login_required
def draft_articles(request):
    template = loader.get_template('dashboard/draft.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

@login_required
def bookmark_articles(request):
    template = loader.get_template('dashboard/bookmark.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

    
class CustomLoginClass(LoginView):
    
    def get_template_names(self):
        if self.request.is_ajax():
            print "LOGS: get_template() LOGIN through ajax "
            return "socialaccount/login.html"
        else:
            print "LOGS: get_template() LOGIN through http request "
            return "account/login.html"
            
    def get_context_data(self, **kwargs):
        ret = super(CustomLoginClass, self).get_context_data(**kwargs)
        if self.request.is_ajax():
            ret.update({"ajax_request": True},)
            print "LOGS: LOGIN through ajax "
        return ret
    
custom_login =  CustomLoginClass.as_view()         