# Generated by Django 4.2 on 2023-05-20 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente_Usuario', '0008_remove_administrador_apellido_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]