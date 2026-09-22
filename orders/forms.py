import re

from django import forms


class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class CustomerDetailsForm(BootstrapFormMixin, forms.Form):
    full_name = forms.CharField(label="Nom complet", max_length=160)
    phone = forms.CharField(label="Numéro de téléphone", max_length=30)
    address = forms.CharField(label="Adresse de livraison", widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields["phone"].widget.attrs.update({"inputmode": "tel", "placeholder": "Ex. 77 123 45 67"})

    def clean_phone(self):
        raw = self.cleaned_data["phone"].strip()
        cleaned = re.sub(r"[^0-9+]", "", raw)
        digits = re.sub(r"\D", "", cleaned)
        if len(digits) < 8 or len(digits) > 15:
            raise forms.ValidationError("Saisissez un numéro de téléphone valide.")
        return cleaned


class DirectOrderForm(CustomerDetailsForm):
    quantity = forms.IntegerField(label="Quantité", min_value=1, max_value=99, initial=1)


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(label="Quantité", min_value=1, max_value=99, initial=1)


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(label="Quantité", min_value=1, max_value=99)
