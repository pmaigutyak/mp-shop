# Generated by Django 2.0.9 on 2020-09-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='new_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Destination name'),
        ),
    ]
