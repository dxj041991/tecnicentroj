# Generated by Django 3.0.4 on 2020-10-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_cliente_correo_electronico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='Direccion',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]