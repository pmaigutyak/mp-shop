# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-22 14:46
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.PositiveIntegerField(choices=[(1, 'Cash payment'), (2, 'Cashless payment'), (3, 'C.O.D.'), (4, 'Privat24 Payment')], default=None, verbose_name='Payment method')),
                ('delivery_method', models.PositiveIntegerField(choices=[(1, 'Self delivery'), (2, 'Nova Poshta'), (7, 'Meest Express'), (6, 'Other')], default=None, verbose_name='Delivery method')),
                ('status', models.PositiveIntegerField(choices=[(0, 'Not reviewed'), (1, 'Processing'), (2, 'Canceled'), (3, 'Completed')], default=0, verbose_name='Status')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('surname', models.CharField(max_length=255, verbose_name='Surname')),
                ('post_office', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address and number of post office')),
                ('mobile', models.CharField(max_length=255, verbose_name='Mobile phone')),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('comment', models.TextField(blank=True, default=b'', max_length=1000, verbose_name='Comment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Product title')),
                ('price', models.FloatField(verbose_name='Price (uah)')),
                ('qty', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='orders.Order', verbose_name='Order')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Order product',
                'verbose_name_plural': 'Order products',
            },
        ),
    ]