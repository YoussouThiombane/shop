import secrets
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from catalog.models import Product


def generate_order_reference():
    date_part = timezone.localdate().strftime("%Y%m%d")
    while True:
        reference = f"MBT-{date_part}-{secrets.token_hex(3).upper()}"
        if not Order.objects.filter(reference=reference).exists():
            return reference


class Order(models.Model):
    class Status(models.TextChoices):
        PREPARATION = "preparation", "En préparation"
        DELIVERED = "delivered", "Livrée"

    reference = models.CharField(max_length=24, unique=True, default=generate_order_reference, editable=False)
    full_name = models.CharField("nom complet", max_length=160)
    phone = models.CharField("téléphone", max_length=30)
    address = models.TextField("adresse")
    status = models.CharField("statut", max_length=20, choices=Status.choices, default=Status.PREPARATION)
    total = models.DecimalField("total", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "commande"
        verbose_name_plural = "commandes"

    def __str__(self):
        return self.reference

    def refresh_total(self):
        self.total = sum((item.subtotal for item in self.items.all()), Decimal("0"))
        self.save(update_fields=["total", "updated_at"])
        return self.total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField("nom du produit", max_length=180)
    unit_price = models.DecimalField("prix unitaire", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("quantité", validators=[MinValueValidator(1)])
    subtotal = models.DecimalField("sous-total", max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "ligne de commande"
        verbose_name_plural = "lignes de commande"

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"
