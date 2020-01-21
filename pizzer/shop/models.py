# -*- coding: utf-8 -*-
import pytils

from django.db import models
from common.fields import JsonField


class Currency(models.Model):
    id = models.PositiveSmallIntegerField('ISO numeric', primary_key=True)
    code = models.CharField('Code (ISO)', max_length=4)
    name = models.CharField('Official name (CAPS)', max_length=128)
    symbol = models.CharField('Symbol', max_length=3, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rate = models.FloatField(default=1.0)
    precision = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ('code', )
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return u'%s' % self.code

    def humanize(self, amount):
        return amount and (float(amount) / self.precision)

    def unhumanize(self, amount):
        return amount and (float(amount) * self.precision)


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
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="products")


class Order(models.Model):
    customer = models.ForeignKey('common.Customer', null=True, on_delete=models.CASCADE, related_name="orders")
    customer_data = JsonField(null=True)
    products_data = JsonField(default=[])
    details = models.TextField(blank=True, null=True)
    currency = models.ForeignKey('catalogue.Currency', default=840, on_delete=models.CASCADE)
    products_price = models.BigIntegerField(null=True)
    # with delivery
    total_price = models.BigIntegerField(null=True)

    delivery_address = models.ForeignKey('common.DeliveryAddress', null=True, on_delete=models.SET_NULL)
    # for nonauthtorized users
    delivery_data = JsonField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
