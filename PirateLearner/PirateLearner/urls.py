from django.conf.urls import *
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from cms.sitemaps import CMSSitemap
from blogging.sitemaps import BlogSitemap,BlogParentSitemap
from bookmarks.sitemaps import BookmarkSitemap
from django.utils.functional import curry
from django.views.defaults import *

# from voting.views import vote_on_object
from blogging.models import BlogContent

tip_dict = {
    'model': BlogContent,
    'template_object_name': 'blogcontent',
    'slug_field': 'slug',
    'allow_xmlhttprequest': 'true',
}

handler500 = curry(server_error, template_name='error_404.html')
handler404 = curry(page_not_found, template_name='error_404.html')
handler403 = curry(permission_denied, template_name='error_404.html')

admin.autodiscover()

urlpatterns = i18n_patterns('',
#    url(r'^polls/', include('polls.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^C/', include('blogging.urls',namespace='blogging')),
    url(r'^dashboard/', include('dashboard.urls',namespace='dashboard')),
    url(r'^bookmarks/', include('bookmarks.urls',namespace='bookmarks')),
    url(r'^spotlight/', include('spotlight.urls',namespace='spotlight')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^user/', include('user_mgmt.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^accounts/login/$', 'dashboard.views.custom_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap,'blog':BlogSitemap,'sections':BlogParentSitemap,
                                                                                  'bookmarks':BookmarkSitemap}}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     url(r"^ratings/", include("agon_ratings.urls")),
    url(r'^rest/', include("rest.urls", namespace="rest")),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
) + staticfiles_urlpatterns() + urlpatterns
