# Generated by Django 3.0.2 on 2020-01-20 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_productcategory_main_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcategory',
            old_name='main_photo',
            new_name='logo',
        ),
    ]