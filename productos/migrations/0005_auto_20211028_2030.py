# Generated by Django 3.2.8 on 2021-10-29 01:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_alter_price_product_date_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_provider',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='ticket_detail',
            name='amount',
        ),
        migrations.AlterField(
            model_name='price_product',
            name='date_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 28, 20, 30, 32, 255947)),
        ),
    ]
