# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from shop.models import Product, ProductOrder, Order, ProductCategory


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
        'created_at', 'customer_data', 'products_data',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
