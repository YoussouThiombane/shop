from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalog.forms import ProductForm, ProductImageFormSet
from catalog.models import Product
from core.forms import SiteSettingsForm
from core.models import SiteSettings
from orders.models import Order

from .decorators import owner_required
from .forms import OrderStatusForm, OwnerProfileForm


@owner_required
def home(request):
    now = timezone.now()
    delivered = Order.objects.filter(status=Order.Status.DELIVERED)
    context = {
        "active_products": Product.objects.filter(is_active=True).count(),
        "total_orders": Order.objects.count(),
        "preparation_orders": Order.objects.filter(status=Order.Status.PREPARATION).count(),
        "delivered_orders": delivered.count(),
        "delivered_revenue": delivered.aggregate(value=Sum("total"))["value"] or Decimal("0"),
        "recent_revenue": delivered.filter(created_at__gte=now - timedelta(days=30)).aggregate(value=Sum("total"))["value"] or Decimal("0"),
        "today_orders": Order.objects.filter(created_at__date=timezone.localdate()).count(),
        "recent_orders": Order.objects.prefetch_related("items")[:6],
    }
    return render(request, "dashboard/home.html", context)


@owner_required
def product_list(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    page_obj = Paginator(products, 12).get_page(request.GET.get("page"))
    return render(request, "dashboard/product_list.html", {"page_obj": page_obj, "query": query})


def _product_form(request, product=None):
    product = product or Product()
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    formset = ProductImageFormSet(
        request.POST or None, request.FILES or None, instance=product, prefix="images"
    )
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        saved_product = form.save()
        formset.instance = saved_product
        formset.save()
        messages.success(request, "Le produit a été enregistré.")
        return redirect("dashboard:products")
    return render(
        request,
        "dashboard/product_form.html",
        {"form": form, "formset": formset, "product": product, "is_edit": bool(product.pk)},
    )


@owner_required
def product_create(request):
    return _product_form(request)


@owner_required
def product_edit(request, pk):
    return _product_form(request, get_object_or_404(Product, pk=pk))


@owner_required
def product_deactivate_confirm(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "dashboard/product_confirm_deactivate.html", {"product": product})


@require_POST
@owner_required
def product_deactivate(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = False
    product.save(update_fields=["is_active", "updated_at"])
    messages.success(request, f"{product.name} a été désactivé.")
    return redirect("dashboard:products")


@owner_required
def order_list(request):
    status = request.GET.get("status", "")
    query = request.GET.get("q", "").strip()
    orders = Order.objects.all()
    if status in Order.Status.values:
        orders = orders.filter(status=status)
    if query:
        orders = orders.filter(Q(reference__icontains=query) | Q(full_name__icontains=query))
    page_obj = Paginator(orders, 15).get_page(request.GET.get("page"))
    return render(request, "dashboard/order_list.html", {"page_obj": page_obj, "status": status, "query": query})


@owner_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk)
    return render(request, "dashboard/order_detail.html", {"order": order, "status_form": OrderStatusForm(instance=order)})


@require_POST
@owner_required
def order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderStatusForm(request.POST, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, "Le statut de la commande a été mis à jour.")
    else:
        messages.error(request, "Le statut sélectionné est invalide.")
    return redirect("dashboard:order_detail", pk=order.pk)


@owner_required
def shop_settings(request):
    instance = SiteSettings.get_solo()
    form = SiteSettingsForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Les informations de la boutique ont été mises à jour.")
        return redirect("dashboard:settings")
    return render(request, "dashboard/settings.html", {"form": form})


@owner_required
def account_settings(request):
    form = OwnerProfileForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Votre profil a été mis à jour.")
        return redirect("dashboard:account")
    return render(request, "dashboard/account.html", {"form": form})


@owner_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Votre mot de passe a été modifié.")
        return redirect("dashboard:account")
    return render(request, "dashboard/password_change.html", {"form": form})
