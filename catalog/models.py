from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField("nom", max_length=180)
    slug = models.SlugField(unique=True, max_length=210, blank=True)
    description = models.TextField("description")
    price = models.DecimalField("prix", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    promotional_price = models.DecimalField(
        "prix promotionnel", max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    main_image = models.ImageField("image principale", upload_to="products/main/", blank=True)
    is_active = models.BooleanField("actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "produit"
        verbose_name_plural = "produits"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:detail", kwargs={"slug": self.slug})

    @property
    def has_promotion(self):
        return self.promotional_price is not None and Decimal("0") < self.promotional_price < self.price

    @property
    def current_price(self):
        return self.promotional_price if self.has_promotion else self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            root = slugify(self.name) or "produit"
            candidate = root
            index = 2
            while Product.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{root}-{index}"
                index += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="additional_images", on_delete=models.CASCADE)
    image = models.ImageField("image", upload_to="products/gallery/")
    order = models.PositiveIntegerField("ordre", default=0)
    alt_text = models.CharField("texte alternatif", max_length=180, blank=True)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "image complémentaire"
        verbose_name_plural = "images complémentaires"

    def __str__(self):
        return f"{self.product.name} — image {self.order}"
