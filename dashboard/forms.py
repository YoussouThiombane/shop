from django import forms

from orders.models import Order


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]


class OwnerProfileForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=150, required=False)
    last_name = forms.CharField(label="Nom", max_length=150, required=False)
    email = forms.EmailField(label="Email", required=False)

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        initial = kwargs.setdefault("initial", {})
        if user:
            initial.update({"first_name": user.first_name, "last_name": user.last_name, "email": user.email})
        super().__init__(*args, **kwargs)

    def save(self):
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        self.user.save(update_fields=["first_name", "last_name", "email"])
        return self.user
