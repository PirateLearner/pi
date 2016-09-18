from django.conf.urls import url, include, handler400
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from blogging.sitemaps import BlogSitemap,BlogParentSitemap
from bookmarks.sitemaps import BookmarkSitemap
from django.utils.functional import curry
from django.views.defaults import *
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from blogging.models import BlogContent
from dashboard.views import custom_login
from blogging.views import ContactUs
from utils import tags

tip_dict = {
    'model': BlogContent,
    'template_object_name': 'blogcontent',
    'slug_field': 'slug',
    'allow_xmlhttprequest': 'true',
}

handler500 = curry(server_error, template_name='error_404.html')
handler404 = curry(page_not_found, template_name='error_404.html')
handler403 = curry(permission_denied, template_name='error_404.html')
handler400 = curry(bad_request, template_name='error_404.html')
sitemaps =  {'blog':BlogSitemap,'sections':BlogParentSitemap,'bookmarks':BookmarkSitemap}

admin.autodiscover()

urlpatterns = i18n_patterns('',
#    url(r'^polls/', include('polls.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^C/', include('blogging.urls',namespace='blogging')),
    url(r'^dashboard/', include('dashboard.urls',namespace='dashboard')),
    url(r'^bookmarks/', include('bookmarks.urls',namespace='bookmarks')),
    url(r'^spotlight/', include('spotlight.urls',namespace='spotlight')),
    url(r'^rest/', include("rest.urls", namespace="rest")),
    url(r'^events/', include("events.urls", namespace="events")),
#    url(r'^voting/', include('voting.urls', namespace='voting')),
#    url(r'^annotations/', include('annotations.urls', namespace='annotations')),
    url(r'^messages/', include("pl_messages.urls", namespace="messages")),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^user/', include('user_mgmt.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/login/$', custom_login),
    url(r'^accounts/logout/$', logout,{'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}),
    url(r'^search/tags/?$', tags, name="tags-ajax"),
    url(r'^contact/?$', ContactUs,name="contact"),
    url(r'^about/?$', TemplateView.as_view(template_name='about.html'),name="about"),
    url(r'^faq/?$', TemplateView.as_view(template_name='faq.html'),name="faq"),
    url(r'^$', TemplateView.as_view(template_name='home.html'),name="home"),
)

# This is only needed when using runserver.
if settings.DEBUG:
#     urlpatterns = patterns('',
#     url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
# ) + staticfiles_urlpatterns() + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
