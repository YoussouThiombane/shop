from django import forms

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["shop_name", "presentation", "whatsapp_number", "contact_email", "address"]
        widgets = {"presentation": forms.Textarea(attrs={"rows": 4})}
