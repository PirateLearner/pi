from django.contrib.sitemaps import Sitemap
from bookmarks.models import BookmarkInstance

class BookmarkSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BookmarkInstance.objects.all()

    def lastmod(self, obj):
        return obj.saved

