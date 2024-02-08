# Generated by Django 5.0.1 on 2024-02-07 20:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dids', '0002_did_error_alter_did_did_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='did',
            name='did_uuid',
            field=models.UUIDField(default=uuid.UUID('d7a4278f-fd0f-46fe-a57c-3546ea367ab1'), unique=True),
        ),
    ]
