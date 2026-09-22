from decimal import Decimal

from catalog.models import Product


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY, {})

    def add(self, product, quantity=1, replace=False):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        self.cart[product_id]["quantity"] = quantity if replace else self.cart[product_id]["quantity"] + quantity
        self.save()

    def remove(self, product):
        self.cart.pop(str(product.pk), None)
        self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.session.modified = True
        self.cart = {}

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        products = Product.objects.filter(pk__in=self.cart.keys(), is_active=True)
        products_by_id = {str(product.pk): product for product in products}
        missing = set(self.cart) - set(products_by_id)
        if missing:
            for product_id in missing:
                self.cart.pop(product_id, None)
            self.save()
        for product_id, stored in self.cart.items():
            product = products_by_id.get(product_id)
            if product is None:
                continue
            quantity = stored["quantity"]
            price = product.current_price
            yield {
                "product": product,
                "quantity": quantity,
                "price": price,
                "subtotal": price * quantity,
            }

    def get_total_price(self):
        return sum((item["subtotal"] for item in self), Decimal("0"))
