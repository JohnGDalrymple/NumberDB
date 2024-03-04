# Generated by Django 4.2.7 on 2024-03-04 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dids', '0007_alter_did_did_uuid_alter_did_error_change_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='did',
            name='did',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='did',
            name='did_uuid',
            field=models.UUIDField(default=uuid.UUID('e91a875a-1079-4577-ae55-ae460ce644e9'), unique=True),
        ),
    ]
