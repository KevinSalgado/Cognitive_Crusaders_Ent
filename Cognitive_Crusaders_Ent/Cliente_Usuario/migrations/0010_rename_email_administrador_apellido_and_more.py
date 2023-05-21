# Generated by Django 4.2 on 2023-05-20 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0009_delete_customuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='administrador',
            old_name='email',
            new_name='apellido',
        ),
        migrations.RenameField(
            model_name='administrador',
            old_name='first_name',
            new_name='contrasena',
        ),
        migrations.RenameField(
            model_name='administrador',
            old_name='last_name',
            new_name='correo',
        ),
        migrations.RenameField(
            model_name='administrador',
            old_name='password1',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='administrador',
            old_name='phone',
            new_name='telefono',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='email',
            new_name='apellido',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='first_name',
            new_name='contrasena',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='last_name',
            new_name='correo',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='password1',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='phone',
            new_name='telefono',
        ),
        migrations.RenameField(
            model_name='trabajador',
            old_name='email',
            new_name='apellido',
        ),
        migrations.RenameField(
            model_name='trabajador',
            old_name='first_name',
            new_name='contrasena',
        ),
        migrations.RenameField(
            model_name='trabajador',
            old_name='last_name',
            new_name='correo',
        ),
        migrations.RenameField(
            model_name='trabajador',
            old_name='password1',
            new_name='nombre',
        ),
        migrations.RemoveField(
            model_name='trabajador',
            name='phone',
        ),
        migrations.AddField(
            model_name='trabajador',
            name='telefono',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
