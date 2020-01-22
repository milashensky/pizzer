# -*- coding: utf-8 -*-
import pytils
from django.db import models

from common.mixins import SerializedView
from common.fields import JsonField


PAYMENT_CASH = 0
PAYMENT_CARD = 1

PAYMENT_METHODS = (
    (PAYMENT_CASH, 'Cash'),
    (PAYMENT_CARD, 'Card')
)


class ProductCategory(models.Model):
    name = models.CharField(max_length=350, unique=True)
    logo = models.OneToOneField('catalogue.Photo', related_name="category_logo", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField()
    price = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey('catalogue.Currency', default=840, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, max_length=200, unique=True)
    photos = models.ManyToManyField('catalogue.Photo', related_name="products")
    main_photo = models.ForeignKey('catalogue.Photo', related_name="product_main_photo", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = pytils.translit.slugify(self.name)
        self.save_base(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def price_humaized(self):
        return self.currency.humanize(self.price)

    @property
    def photo_urls(self):
        urls = []
        if self.main_photo:
            urls.append(self.main_photo.photo.url)
        for photo in self.photos.all().exclude(id=self.main_photo_id):
            urls.append(photo.photo.url)
        return urls


class ProductOrder(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="products", null=True)

    @property
    def serialized(self):
        fields = ('id', 'slug', 'name', 'description', 'currency_id', 'price')
        return {'quantity': self.quantity, **SerializedView.serialize_item(self.product, fields)}

    def __str__(self):
        return '%s: %s' % (self.product_id, self.quantity)


class Order(models.Model):
    customer = models.ForeignKey('common.Customer', null=True, on_delete=models.CASCADE, related_name="orders")
    customer_data = JsonField(null=True)
    products_data = JsonField(default=[])
    details = models.TextField(blank=True, null=True)
    currency = models.ForeignKey('catalogue.Currency', default=840, on_delete=models.CASCADE)
    products_price = models.BigIntegerField()
    # with delivery
    total_price = models.BigIntegerField()
    delivery_address = models.ForeignKey('common.DeliveryAddress', null=True, on_delete=models.SET_NULL)
    # for nonauthtorized users
    delivery_data = JsonField(null=True)
    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s as %s' % (self.customer_id, self.customer_data.get('name'), self.created_at)
