# Generated by Django 3.1.2 on 2024-06-01 06:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time_placed',
            field=models.TimeField(default=datetime.time(12, 0, 37, 871074)),
        ),
    ]
