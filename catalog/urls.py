from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [path("<slug:slug>/", views.product_detail, name="detail")]
