from django import forms
from django.forms import inlineformset_factory

from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "slug", "description", "price", "promotional_price", "main_image", "is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}
        help_texts = {"slug": "Laissez vide pour le générer automatiquement. Il restera stable ensuite."}

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        promotional = cleaned.get("promotional_price")
        if price is not None and price <= 0:
            self.add_error("price", "Le prix doit être strictement positif.")
        if promotional is not None and promotional <= 0:
            self.add_error("promotional_price", "Le prix promotionnel doit être strictement positif.")
        return cleaned


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=["image", "order", "alt_text"],
    extra=3,
    can_delete=True,
    widgets={"alt_text": forms.TextInput(attrs={"placeholder": "Ex. Vue du flacon"})},
)
