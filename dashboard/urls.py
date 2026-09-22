from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("produits/", views.product_list, name="products"),
    path("produits/nouveau/", views.product_create, name="product_create"),
    path("produits/<int:pk>/modifier/", views.product_edit, name="product_edit"),
    path("produits/<int:pk>/desactiver/", views.product_deactivate_confirm, name="product_deactivate_confirm"),
    path("produits/<int:pk>/desactiver/confirmer/", views.product_deactivate, name="product_deactivate"),
    path("commandes/", views.order_list, name="orders"),
    path("commandes/<int:pk>/", views.order_detail, name="order_detail"),
    path("commandes/<int:pk>/statut/", views.order_status, name="order_status"),
    path("reglages/", views.shop_settings, name="settings"),
    path("mon-compte/", views.account_settings, name="account"),
    path("mon-compte/mot-de-passe/", views.password_change, name="password_change"),
]
