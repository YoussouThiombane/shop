import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import Order, OrderItem

logger = logging.getLogger("orders")


@transaction.atomic
def create_order(*, full_name, phone, address, lines):
    """Create an order using immutable price/name snapshots."""
    order = Order.objects.create(full_name=full_name, phone=phone, address=address)
    for line in lines:
        product = line["product"]
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            unit_price=product.current_price,
            quantity=line["quantity"],
            subtotal=product.current_price * line["quantity"],
        )
    order.refresh_total()
    return order


def notify_owner(order):
    """Notify the owner; email failure never changes the saved order."""
    if not settings.OWNER_ORDER_EMAIL:
        logger.info("Commande %s créée; OWNER_ORDER_EMAIL n'est pas configuré.", order.reference)
        return False
    lines = [
        f"Nouvelle commande {order.reference}",
        f"Client : {order.full_name}",
        f"Téléphone : {order.phone}",
        f"Adresse : {order.address}",
        "",
        "Articles :",
    ]
    lines.extend(f"- {item.product_name} × {item.quantity} : {item.subtotal:.0f} FCFA" for item in order.items.all())
    lines.extend(["", f"Total : {order.total:.0f} FCFA", f"Reçue le : {timezone.localtime(order.created_at):%d/%m/%Y à %H:%M}"])
    try:
        send_mail(
            subject=f"Nouvelle commande {order.reference}",
            message="\n".join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.OWNER_ORDER_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception("Échec de l'envoi de l'email pour la commande %s", order.reference)
        return False
