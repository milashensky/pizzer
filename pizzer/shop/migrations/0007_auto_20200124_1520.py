# Generated by Django 3.0.2 on 2020-01-24 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200121_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
