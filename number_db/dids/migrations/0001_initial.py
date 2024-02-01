# Generated by Django 4.2.7 on 2024-02-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Did',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('did', models.BigIntegerField()),
                ('customer', models.CharField(blank=True, max_length=30, null=True)),
                ('reseller', models.CharField(blank=True, max_length=30, null=True)),
                ('in_method', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=2, null=True)),
                ('status', models.CharField(blank=True, choices=[('A', 'Active'), ('D', 'Disco')], max_length=2, null=True)),
                ('change_date', models.DateField(blank=True, null=True, verbose_name='%m/%d/%Y')),
                ('voice_carrier', models.CharField(blank=True, choices=[('IW', 'INTQ - Wholesale'), ('IO', 'INTQ - OC'), ('TWI', 'Twilio')], max_length=3, null=True)),
                ('type', models.CharField(blank=True, choices=[('F', 'Fusion'), ('T', 'Teams'), ('HS', 'Hosted SMS'), ('PK', 'Parked'), ('IV', 'Inventory'), ('EF', 'Efax'), ('OP', 'Orphaned'), ('CL', 'Comelit')], max_length=2, null=True)),
                ('sms_enabled', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=2, null=True)),
                ('sms_carrier', models.CharField(blank=True, choices=[('INTQ', 'INTQ'), ('TWL', 'Twilio')], max_length=4, null=True)),
                ('sms_type', models.CharField(blank=True, choices=[('YP', 'Yak Personal'), ('YS', 'Yak Shared'), ('YB', 'Yak Personal and Shared'), ('IA', 'INTQ API'), ('CL', 'Clerk'), ('SI', 'SIP/Simple')], max_length=2, null=True)),
                ('sms_campaign', models.CharField(blank=True, max_length=20, null=True)),
                ('term_location', models.CharField(blank=True, choices=[('SE', 'SBC - East'), ('SW', 'SBC - West'), ('HE', 'Hosted - East'), ('HW', 'Hosted - West'), ('OC', 'OP - Operator Connect')], max_length=2, null=True)),
                ('user_first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('user_last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('extension', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=30, null=True)),
                ('onboard_date', models.DateField(blank=True, null=True, verbose_name='%m/%d/%Y')),
                ('note', models.TextField(blank=True, max_length=255, null=True)),
                ('e911_enabled_billed', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=2, null=True)),
                ('e911_cid', models.BigIntegerField(blank=True, null=True)),
                ('e911_address', models.TextField(blank=True, max_length=150, null=True)),
                ('did_uuid', models.TextField(max_length=50, unique=True)),
                ('service_1', models.TextField(blank=True, max_length=100, null=True)),
                ('service_2', models.TextField(blank=True, max_length=100, null=True)),
                ('service_3', models.TextField(blank=True, max_length=100, null=True)),
                ('service_4', models.TextField(blank=True, max_length=100, null=True)),
                ('updated_date_time', models.DateField(blank=True, null=True, verbose_name='%m/%d/%Y %H:%M:%S')),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
