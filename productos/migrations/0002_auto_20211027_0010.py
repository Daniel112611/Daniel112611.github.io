# Generated by Django 3.2.8 on 2021-10-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price_product',
            old_name='star_date',
            new_name='start_date',
        ),
        migrations.AlterField(
            model_name='price_product',
            name='date_update',
            field=models.DateTimeField(),
        ),
    ]