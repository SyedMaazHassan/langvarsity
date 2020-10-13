# Generated by Django 3.1 on 2020-10-08 15:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_auto_20201008_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='IN-PROCESS', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 8, 20, 4, 1, 298135)),
        ),
    ]
