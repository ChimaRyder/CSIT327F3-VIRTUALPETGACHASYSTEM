# Generated by Django 5.1.1 on 2024-10-27 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_inventory_is_busy'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='date_acquired',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 27, 6, 12, 3, 66825, tzinfo=datetime.timezone.utc)),
        ),
    ]
