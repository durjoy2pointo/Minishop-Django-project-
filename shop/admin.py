from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Address, Order, OrderItem, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'image_preview',
        'title',
        'gender',
        'category',
        'price',
        'discount_price',
        'created_at',
        'updated_at',
    ]

    list_filter = ['gender', 'category']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def image_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;" />',
                obj.picture.url
            )
        return "No Image"

    image_preview.short_description = 'Picture'

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'address_type',
        'contact_number',
        'division',
        'district',
        'thana',
        'corporation_or_union',
        'area_or_village',
        'additional_info',
    )

    list_filter = (
        'address_type',
        'division',
        'district',
    )

    search_fields = (
        'user__username',
        'contact_number',
        'division',
        'district',
        'thana',
        'area_or_village',
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'product',
        'quantity',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'address',
        'payment_method',
        'total_price',
        'status',
        'created_at',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
    )