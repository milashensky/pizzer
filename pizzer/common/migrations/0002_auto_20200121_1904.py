# Generated by Django 3.0.2 on 2020-01-21 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryaddress',
            old_name='details',
            new_name='address',
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='appartaments',
            field=models.CharField(default='', max_length=70),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='house',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]