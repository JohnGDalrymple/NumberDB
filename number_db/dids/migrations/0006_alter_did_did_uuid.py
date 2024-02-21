# Generated by Django 5.0.1 on 2024-02-20 18:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dids', '0005_alter_did_did_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='did',
            name='did_uuid',
            field=models.UUIDField(default=uuid.UUID('25b954ed-4e43-41d9-b989-697a256d8244'), unique=True),
        ),
    ]
