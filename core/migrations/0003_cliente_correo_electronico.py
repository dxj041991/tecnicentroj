# Generated by Django 2.2.7 on 2020-12-29 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_cliente_correo_electronico'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='Correo_electronico',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]