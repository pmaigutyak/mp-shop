# Generated by Django 3.0.10 on 2020-10-06 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Category title'),
        ),
    ]
