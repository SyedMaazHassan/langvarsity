# Generated by Django 3.1 on 2020-10-06 07:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 6, 12, 23, 0, 898590)),
        ),
    ]
