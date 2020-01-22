# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction

from common.mixins import SerializedView
from shop.models import Product
from shop.forms import CreateOrderForm


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


class OrderApi(SerializedView):
    fields = ('id', 'delivery_data', 'customer_data', 'products_data', 'created_at', 'currency_id:currency', 'total_price', 'products_price')

    def get(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'customer'):
            page = int(request.GET.get('page', 0))
            per_page = int(request.GET.get('per_page', 20))
            current = page * per_page
            qs = request.user.customer.orders.all().order_by('-created_at')
            return {'orders': self.serialize_items(qs[current:current + per_page], self.fields), 'total': qs.count()}
        raise PermissionDenied

    @transaction.atomic
    def post(self, request):
        self.data['user'] = request.user
        sid = transaction.savepoint()
        form = CreateOrderForm(self.data)
        if form.is_valid():
            order = form.save()
            transaction.savepoint_commit(sid)
            if not request.user.is_authenticated and form.data.get('user_created'):
                login(request, order.customer.user)
            return {'state': True, 'id': order.id}
        transaction.savepoint_rollback(sid)
        return {'state': False, 'errors': form.errors}
