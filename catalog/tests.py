from decimal import Decimal

from django.test import TestCase

from .models import Product


class ProductModelTests(TestCase):
    def test_generated_slug_is_unique_and_stable(self):
        first = Product.objects.create(name="Sérum Éclat", description="A", price=Decimal("10000"))
        second = Product.objects.create(name="Sérum Éclat", description="B", price=Decimal("12000"))
        self.assertEqual(first.slug, "serum-eclat")
        self.assertEqual(second.slug, "serum-eclat-2")
        first.name = "Nouveau nom"
        first.save()
        self.assertEqual(first.slug, "serum-eclat")

    def test_promotion_only_applies_when_valid(self):
        product = Product(name="Crème", price=Decimal("10000"), promotional_price=Decimal("7500"))
        self.assertTrue(product.has_promotion)
        self.assertEqual(product.current_price, Decimal("7500"))
        product.promotional_price = Decimal("12000")
        self.assertFalse(product.has_promotion)
        self.assertEqual(product.current_price, Decimal("10000"))
