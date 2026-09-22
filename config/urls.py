from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import ProductSitemap, StaticViewSitemap

sitemaps = {"static": StaticViewSitemap, "products": ProductSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("produits/", include("catalog.urls")),
    path("panier/", include("orders.urls")),
    path("compte/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
