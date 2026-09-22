from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from catalog.models import Product

from .models import Order


class OrderingFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Huile précieuse", description="Soin", price=Decimal("15000"), promotional_price=Decimal("12000")
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse("orders:add", args=[self.product.pk]), {"quantity": 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["cart"][str(self.product.pk)]["quantity"], 2)

    @override_settings(OWNER_ORDER_EMAIL="")
    def test_direct_order_snapshots_price_and_calculates_total(self):
        response = self.client.post(
            reverse("orders:direct_order", args=[self.product.slug]),
            {"full_name": "Awa Ndiaye", "phone": "77 123 45 67", "address": "Dakar", "quantity": 3},
        )
        order = Order.objects.get()
        self.assertRedirects(response, reverse("orders:confirmation", args=[order.reference]))
        self.assertEqual(order.total, Decimal("36000"))
        item = order.items.get()
        self.assertEqual(item.product_name, self.product.name)
        self.assertEqual(item.unit_price, Decimal("12000"))

    @override_settings(OWNER_ORDER_EMAIL="")
    def test_cart_checkout_clears_cart(self):
        self.client.post(reverse("orders:add", args=[self.product.pk]), {"quantity": 2})
        response = self.client.post(
            reverse("orders:checkout"),
            {"full_name": "Mame Fall", "phone": "76 000 00 00", "address": "Thiès"},
        )
        order = Order.objects.get()
        self.assertEqual(order.total, Decimal("24000"))
        self.assertEqual(self.client.session.get("cart", {}), {})
        self.assertRedirects(response, reverse("orders:confirmation", args=[order.reference]))

    @override_settings(OWNER_ORDER_EMAIL="owner@example.com")
    @patch("orders.services.send_mail", side_effect=OSError("SMTP indisponible"))
    def test_email_failure_does_not_cancel_order(self, mocked_send):
        response = self.client.post(
            reverse("orders:direct_order", args=[self.product.slug]),
            {"full_name": "Awa Ndiaye", "phone": "771234567", "address": "Dakar", "quantity": 1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        mocked_send.assert_called_once()

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="shop@example.com",
        OWNER_ORDER_EMAIL="owner@example.com",
    )
    def test_owner_email_contains_order_details(self):
        self.client.post(
            reverse("orders:direct_order", args=[self.product.slug]),
            {"full_name": "Awa Ndiaye", "phone": "771234567", "address": "Dakar", "quantity": 2},
        )
        order = Order.objects.get()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertIn(order.reference, message.subject)
        self.assertIn("Awa Ndiaye", message.body)
        self.assertIn(self.product.name, message.body)
        self.assertIn("24000 FCFA", message.body)
