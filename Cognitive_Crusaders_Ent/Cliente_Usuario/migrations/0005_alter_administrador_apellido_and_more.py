# Generated by Django 4.2 on 2023-05-19 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0004_alter_pedido_alcance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrador',
            name='apellido',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='administrador',
            name='contrasena',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='administrador',
            name='correo',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='administrador',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='Observaciones',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='contrasena',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='rol',
            name='descripcion',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='rol',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='Especialidad',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='apellido',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='contrasena',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='correo',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
    ]
