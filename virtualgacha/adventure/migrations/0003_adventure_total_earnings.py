# Generated by Django 4.2.12 on 2024-10-27 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_adventure_is_claimed'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventure',
            name='total_earnings',
            field=models.FloatField(default=0),
        ),
    ]