# Generated by Django 3.1 on 2020-10-06 09:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_auto_20201006_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='file_type',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 6, 14, 34, 30, 568458)),
        ),
    ]