# Generated by Django 3.0.2 on 2020-01-20 14:15

import common.fields
import common.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChunkedPhotoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('format', models.CharField(default='', max_length=64)),
                ('data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='ISO numeric')),
                ('code', models.CharField(max_length=4, verbose_name='Code (ISO)')),
                ('name', models.CharField(max_length=128, verbose_name='Official name (CAPS)')),
                ('symbol', models.CharField(blank=True, max_length=3, null=True, verbose_name='Symbol')),
                ('is_active', models.BooleanField(default=True)),
                ('rate', models.FloatField(default=1.0)),
                ('precision', models.PositiveSmallIntegerField(default=100)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='DeliveryArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(upload_to=common.utils.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='LayoutTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('slug', models.SlugField(max_length=500)),
                ('structure', common.fields.JsonField()),
                ('preview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme_preview', to='catalogue.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('slug', models.SlugField(max_length=500)),
                ('type', models.TextField()),
                ('path', models.TextField()),
                ('preview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme_element_preview', to='catalogue.Photo')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='catalogue.LayoutTheme')),
            ],
            options={
                'unique_together': {('slug', 'theme')},
            },
        ),
    ]