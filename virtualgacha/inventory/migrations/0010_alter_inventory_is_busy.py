# Generated by Django 4.2.12 on 2024-10-27 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_remove_inventory_pet_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='is_busy',
            field=models.IntegerField(choices=[(0, 'Not Busy'), (1, 'Busy'), (2, 'On Market')]),
        ),
    ]
