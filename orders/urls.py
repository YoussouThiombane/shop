from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.cart_detail, name="cart"),
    path("ajouter/<int:product_id>/", views.cart_add, name="add"),
    path("modifier/<int:product_id>/", views.cart_update, name="update"),
    path("supprimer/<int:product_id>/", views.cart_remove, name="remove"),
    path("commander/", views.checkout, name="checkout"),
    path("commande-directe/<slug:slug>/", views.direct_order, name="direct_order"),
    path("confirmation/<str:reference>/", views.confirmation, name="confirmation"),
]
