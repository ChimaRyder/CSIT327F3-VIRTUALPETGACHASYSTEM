# Generated by Django 4.2.12 on 2024-10-27 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_pet_rarity'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='pet_rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
