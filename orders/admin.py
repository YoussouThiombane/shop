from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "unit_price", "quantity", "subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["reference", "full_name", "status", "total", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["reference", "full_name", "phone"]
    inlines = [OrderItemInline]
