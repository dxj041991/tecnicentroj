# Generated by Django 3.0.4 on 2020-10-16 12:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201001_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]