from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from orders.models import Order


class DashboardSecurityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="owner", password="Strong-test-pass-2026")

    def test_private_view_redirects_anonymous_user(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:home')}")

    def test_private_view_has_strict_no_cache_headers(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store, no-cache, must-revalidate, max-age=0")
        self.assertEqual(response["Pragma"], "no-cache")
        self.assertEqual(response["Expires"], "0")

    def test_order_status_can_be_changed(self):
        order = Order.objects.create(full_name="Client", phone="771234567", address="Dakar", total=Decimal("1000"))
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("dashboard:order_status", args=[order.pk]), {"status": Order.Status.DELIVERED}
        )
        order.refresh_from_db()
        self.assertRedirects(response, reverse("dashboard:order_detail", args=[order.pk]))
        self.assertEqual(order.status, Order.Status.DELIVERED)
