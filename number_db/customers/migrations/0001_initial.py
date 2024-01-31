# Generated by Django 4.2.7 on 2024-01-31 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('fax', models.CharField(blank=True, max_length=30, null=True)),
                ('mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=30, null=True)),
                ('billing_address', models.CharField(blank=True, max_length=150, null=True)),
                ('billing_city', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_state', models.CharField(blank=True, max_length=10, null=True)),
                ('billing_zipcode', models.CharField(blank=True, max_length=20, null=True)),
                ('billing_country', models.CharField(blank=True, max_length=20, null=True)),
                ('e911_address', models.CharField(blank=True, max_length=150, null=True)),
                ('e911_city', models.CharField(blank=True, max_length=50, null=True)),
                ('e911_state', models.CharField(blank=True, max_length=10, null=True)),
                ('e911_zipcode', models.CharField(blank=True, max_length=20, null=True)),
                ('e911_country', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
