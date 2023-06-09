# Generated by Django 4.2 on 2023-05-21 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0010_rename_email_administrador_apellido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrador',
            name='fk_Rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Cliente_Usuario.rol'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fk_Rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Cliente_Usuario.rol'),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='fk_Rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Cliente_Usuario.rol'),
        ),
    ]
