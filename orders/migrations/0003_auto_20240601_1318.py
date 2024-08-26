# Generated by Django 3.1.2 on 2024-06-01 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20240601_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_charge',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_placed',
            field=models.TimeField(default=datetime.time(13, 17, 59, 977476)),
        ),
    ]
