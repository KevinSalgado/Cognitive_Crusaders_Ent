# Generated by Django 4.2 on 2023-05-11 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0002_pedido_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidotrabajador',
            name='Fecha_Aceptado',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='trabajador',
            name='Especialidad',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trabajador',
            name='Fecha_Ingreso',
            field=models.DateField(null=True),
        ),
    ]
