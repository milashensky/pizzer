# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from shop.models import Currency, Product, ProductOrder, Order, ProductCategory


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "rate")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'description', 'category', 'currency', 'main_photo',
    )


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ("quantity", "product", "order")


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer', 'customer_data', 'products_data', 'details', 'currency', 'products_price', 'total_price', 'delivery_address', 'delivery_data',
    )


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
