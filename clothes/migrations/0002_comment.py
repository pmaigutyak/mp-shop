# Generated by Django 3.0.13 on 2021-07-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryprofile',
            options={'verbose_name': 'Category profile', 'verbose_name_plural': 'Category profiles'},
        ),
        migrations.AddField(
            model_name='clothessize',
            name='comment',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Comment'),
        ),
    ]
