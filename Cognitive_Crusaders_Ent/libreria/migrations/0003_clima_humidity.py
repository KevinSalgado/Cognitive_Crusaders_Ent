# Generated by Django 4.2 on 2023-06-13 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0002_clima'),
    ]

    operations = [
        migrations.AddField(
            model_name='clima',
            name='humidity',
            field=models.FloatField(default=1, verbose_name='humidity'),
            preserve_default=False,
        ),
    ]
