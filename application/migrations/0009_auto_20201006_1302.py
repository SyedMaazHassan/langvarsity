# Generated by Django 3.1 on 2020-10-06 08:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20201006_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 6, 13, 2, 41, 770855)),
        ),
    ]
