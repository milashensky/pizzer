# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from common.mixins import SerializedView
from shop.models import Product


class ProductApi(SerializedView):
    fields = ('id', 'slug', 'name', 'description', 'price', 'currency_id:currency', 'main_photo__photo__url:preview')

    def get_item(self, slug):
        self.fields = self.fields + ({'photos': ('photo__url:url', 'id')}, )
        return get_object_or_404(Product, slug=slug)

    def get(self, request, slug=None):
        if slug:
            return self.get_item(slug)
        return Product.objects.all()


class CategoryApi(SerializedView):
    fields = ('id', 'name', 'logo__photo__url:preview')

    def get(self, request):
        return Product.objects.all()
