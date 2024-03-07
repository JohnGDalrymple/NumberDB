# Generated by Django 4.2.7 on 2024-03-07 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0005_service_order_customer_service_order_e911_cid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service_order',
            name='e911_cid',
        ),
        migrations.AlterField(
            model_name='service_order',
            name='e911_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
