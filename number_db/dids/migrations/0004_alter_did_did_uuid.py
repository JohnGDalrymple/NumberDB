# Generated by Django 4.2.7 on 2024-02-13 15:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dids', '0003_alter_did_did_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='did',
            name='did_uuid',
            field=models.UUIDField(default=uuid.UUID('e3b82143-e633-4f27-a794-948c119388db'), unique=True),
        ),
    ]
