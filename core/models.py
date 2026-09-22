from django.db import models


class SiteSettings(models.Model):
    shop_name = models.CharField("nom de la boutique", max_length=120, default="Mbécté Trading")
    presentation = models.TextField(
        "texte de présentation",
        default="Des essentiels beauté sélectionnés avec soin pour révéler votre éclat naturel.",
    )
    whatsapp_number = models.CharField("numéro WhatsApp affiché", max_length=30, default="70 207 39 07")
    contact_email = models.EmailField("email de contact", blank=True)
    address = models.CharField("adresse / informations complémentaires", max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "paramètres de la boutique"
        verbose_name_plural = "paramètres de la boutique"

    def __str__(self):
        return self.shop_name

    @classmethod
    def get_solo(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return None
