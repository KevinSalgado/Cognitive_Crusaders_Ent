# Generated by Django 4.2 on 2023-05-12 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0003_remove_pedido_fk_estado_delete_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='Alcance',
            field=models.CharField(max_length=200),
        ),
    ]