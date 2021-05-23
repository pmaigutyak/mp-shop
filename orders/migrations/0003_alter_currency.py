# Generated by Django 3.0.13 on 2021-05-23 07:35

from django.db import migrations
import exchange.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='initial_currency',
            field=exchange.models.CurrencyField(choices=[(980, 'UAH'), (840, 'USD'), (978, 'EUR')], default=980, verbose_name='Currency'),
        ),
    ]