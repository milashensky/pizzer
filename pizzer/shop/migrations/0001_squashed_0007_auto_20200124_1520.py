# Generated by Django 3.0.2 on 2020-01-24 15:24

import common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('shop', '0001_initial'), ('shop', '0002_auto_20200120_1458'), ('shop', '0003_productcategory_main_photo'), ('shop', '0004_auto_20200120_1514'), ('shop', '0005_auto_20200121_1904'), ('shop', '0006_auto_20200121_2138'), ('shop', '0007_auto_20200124_1520')]

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
        ('catalogue', '0002_auto_20200120_1458'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('logo', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='category_logo', to='catalogue.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.BigIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.ProductCategory')),
                ('currency', models.ForeignKey(default=840, on_delete=django.db.models.deletion.CASCADE, to='catalogue.Currency')),
                ('main_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_main_photo', to='catalogue.Photo')),
                ('photos', models.ManyToManyField(related_name='products', to='catalogue.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_data', common.fields.JsonField(null=True)),
                ('products_data', common.fields.JsonField(default=[])),
                ('details', models.TextField(blank=True, null=True)),
                ('products_price', models.BigIntegerField(default=0)),
                ('total_price', models.BigIntegerField(default=0)),
                ('delivery_data', common.fields.JsonField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(default=840, on_delete=django.db.models.deletion.CASCADE, to='catalogue.Currency')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='common.Customer')),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.DeliveryAddress')),
                ('payment_method', models.PositiveSmallIntegerField(choices=[(0, 'Cash'), (1, 'Card')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='shop.Product')),
            ],
        ),
    ]
