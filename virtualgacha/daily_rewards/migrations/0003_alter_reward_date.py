# Generated by Django 5.1.2 on 2024-11-02 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_rewards', '0002_reward_pet_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='date',
            field=models.DateField(default=datetime.date.today, unique=True),
        ),
    ]