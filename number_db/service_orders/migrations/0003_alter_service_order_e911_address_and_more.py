# Generated by Django 5.0.1 on 2024-02-26 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0002_service_order_e911_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_order',
            name='e911_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='service_order',
            name='e911_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
