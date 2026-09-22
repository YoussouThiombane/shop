from django.shortcuts import get_object_or_404, render

from orders.forms import DirectOrderForm

from .models import Product


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("additional_images"), slug=slug, is_active=True
    )
    return render(request, "catalog/product_detail.html", {"product": product, "direct_form": DirectOrderForm()})
