# Generated by Django 4.2.12 on 2024-10-27 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_pet_is_busy_inventory_is_busy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='pet_rate',
        ),
        migrations.AddField(
            model_name='inventory',
            name='pet_rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
