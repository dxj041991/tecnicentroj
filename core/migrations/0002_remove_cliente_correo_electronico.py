# Generated by Django 2.2.7 on 2020-12-29 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='Correo_electronico',
        ),
    ]