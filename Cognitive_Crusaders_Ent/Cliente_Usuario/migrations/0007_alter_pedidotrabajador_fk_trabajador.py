# Generated by Django 4.2 on 2023-05-20 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0006_alter_pedido_fk_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidotrabajador',
            name='fk_Trabajador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Cliente_Usuario.trabajador'),
        ),
    ]