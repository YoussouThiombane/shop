from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


def home(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")[:12]
    return render(request, "core/home.html", {"products": products})


def robots_txt(request):
    content = "User-agent: *\nAllow: /\nDisallow: /dashboard/\nDisallow: /compte/\nSitemap: {}\n".format(
        request.build_absolute_uri("/sitemap.xml")
    )
    return HttpResponse(content, content_type="text/plain")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
