from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.sitemaps import StaticViewSitemap, ReferenceCaseSitemap
from django.contrib.sitemaps.views import sitemap
from core import views as core_views

sitemaps = {
    "static": StaticViewSitemap,
    "references": ReferenceCaseSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", core_views.robots_txt, name="robots.txt"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
