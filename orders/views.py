from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from catalog.models import Product

from .cart import Cart
from .forms import CartAddForm, CartUpdateForm, CustomerDetailsForm, DirectOrderForm
from .models import Order
from .services import create_order, notify_owner


def _safe_next(request, fallback):
    candidate = request.POST.get("next", "")
    if candidate and url_has_allowed_host_and_scheme(candidate, allowed_hosts={request.get_host()}):
        return candidate
    return fallback


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    form = CartAddForm(request.POST)
    if form.is_valid():
        Cart(request).add(product, quantity=form.cleaned_data["quantity"])
        messages.success(request, f"{product.name} a été ajouté au panier.")
    else:
        messages.error(request, "La quantité demandée est invalide.")
    return redirect(_safe_next(request, reverse("orders:cart")))


def cart_detail(request):
    return render(request, "orders/cart.html", {"cart": Cart(request)})


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    form = CartUpdateForm(request.POST)
    if form.is_valid():
        Cart(request).add(product, quantity=form.cleaned_data["quantity"], replace=True)
        messages.success(request, "La quantité a été mise à jour.")
    else:
        messages.error(request, "La quantité demandée est invalide.")
    return redirect("orders:cart")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).remove(product)
    messages.success(request, "Le produit a été retiré du panier.")
    return redirect("orders:cart")


def checkout(request):
    cart = Cart(request)
    cart_lines = list(cart)
    if not cart_lines:
        messages.info(request, "Votre panier est vide.")
        return redirect("orders:cart")
    form = CustomerDetailsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = create_order(lines=cart_lines, **form.cleaned_data)
        cart.clear()
        notify_owner(order)
        return redirect("orders:confirmation", reference=order.reference)
    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@require_POST
def direct_order(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    form = DirectOrderForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data.copy()
        quantity = data.pop("quantity")
        order = create_order(lines=[{"product": product, "quantity": quantity}], **data)
        notify_owner(order)
        return redirect("orders:confirmation", reference=order.reference)
    messages.error(request, "Vérifiez les informations de commande indiquées.")
    return render(request, "catalog/product_detail.html", {"product": product, "direct_form": form}, status=400)


def confirmation(request, reference):
    order = get_object_or_404(Order, reference=reference)
    return render(request, "orders/confirmation.html", {"order": order})
