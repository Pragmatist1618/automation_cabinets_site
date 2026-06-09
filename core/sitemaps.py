from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import ReferenceCase

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "references", "contacts"]

    def location(self, item):
        return reverse(item)

class ReferenceCaseSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return ReferenceCase.objects.filter(is_published=True)

    def location(self, item):
        return item.get_absolute_url()
