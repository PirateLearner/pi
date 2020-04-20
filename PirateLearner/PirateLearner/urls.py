from django.conf.urls import url, handler400
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static

from blogging.sitemaps import BlogSitemap,BlogParentSitemap
from bookmarks.sitemaps import BookmarkSitemap
from functools import partialmethod
from django.views.defaults import *

from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from blogging.models import BlogContent
from dashboard.views import custom_login
from blogging.views import ContactUs
from PirateLearner.utils import tags

app_name="core"

tip_dict = {
    'model': BlogContent,
    'template_object_name': 'blogcontent',
    'slug_field': 'slug',
    'allow_xmlhttprequest': 'true',
}

ERROR_404_TEMPLATE_NAME = 'error_404.html'
ERROR_500_TEMPLATE_NAME = 'error_404.html'
ERROR_403_TEMPLATE_NAME = 'error_404.html'
ERROR_400_TEMPLATE_NAME = 'error_404.html'
#handler500 = partialmethod(server_error, template_name='error_404.html')
#handler404 = partialmethod(page_not_found, template_name='error_404.html')
#handler403 = partialmethod(permission_denied, template_name='error_404.html')
#handler400 = partialmethod(bad_request, template_name='error_404.html')
sitemaps =  {'blog':BlogSitemap,'sections':BlogParentSitemap,'bookmarks':BookmarkSitemap}

admin.autodiscover()

urlpatterns = i18n_patterns(
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('C/', include('blogging.urls', namespace='blogging'), name='blogging'),
    path('dashboard/', include('dashboard.urls',namespace='dashboard'), name='dashboard'),
    path('bookmarks/', include('bookmarks.urls',namespace='bookmarks'), name='bookmarks'),
    path('spotlight/', include('spotlight.urls',namespace='spotlight'), name='spotlight'),
    path('rest/', include("rest.urls", namespace="rest")),
    path('events/', include("events.urls", namespace="events")),
#    path('voting/', include('voting.urls', namespace='voting')),
#    path('annotations/', include('annotations.urls', namespace='annotations')),
    path('messages/', include("pl_messages.urls", namespace="messages"), name='messages'),
    path('admin/', admin.site.urls),
    #path('user/', include('user_mgmt.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/login/', custom_login),
    path('accounts/logout/', LogoutView.as_view(),{'next_page': '/'}),
    path('accounts/', include('allauth.urls')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}),
    re_path(r'^search/tags/?$', tags, name="tags-ajax"),
    re_path(r'^contact/?$', ContactUs,name="contact"),
    re_path(r'^about/?$', TemplateView.as_view(template_name='about.html'),name="about"),
    re_path(r'^faq/?$', TemplateView.as_view(template_name='faq.html'),name="faq"),
    re_path(r'^search/?$', TemplateView.as_view(template_name='site-search.html'),name="site-search"),
    path('', TemplateView.as_view(template_name='home.html'),name="home"),
)

# This is only needed when using runserver.
if settings.DEBUG:
#     urlpatterns = patterns('',
#     url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
# ) + staticfiles_urlpatterns() + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
