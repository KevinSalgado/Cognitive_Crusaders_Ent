# Generated by Django 4.2 on 2023-05-11 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='Status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
