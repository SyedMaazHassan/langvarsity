# Generated by Django 3.1 on 2020-10-08 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20201008_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 8, 19, 58, 11, 87854)),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='IN-PROCESS', max_length=20),
        ),
    ]