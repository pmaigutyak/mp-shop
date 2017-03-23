# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-22 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('title_uk', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Product flag',
                'verbose_name_plural': 'Product flags',
            },
        ),
    ]