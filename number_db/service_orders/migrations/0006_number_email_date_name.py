# Generated by Django 4.2.7 on 2024-03-26 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0005_alter_number_email_date_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='number_email_date',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
