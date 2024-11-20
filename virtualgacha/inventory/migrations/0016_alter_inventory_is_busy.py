# Generated by Django 5.1.2 on 2024-11-03 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_alter_inventory_date_acquired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='is_busy',
            field=models.IntegerField(choices=[(0, 'Not Busy'), (1, 'Busy'), (2, 'On Market')], default=0),
        ),
    ]