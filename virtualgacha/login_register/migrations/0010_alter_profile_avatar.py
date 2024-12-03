# Generated by Django 5.1.2 on 2024-12-03 12:42

import login_register.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0009_profile_uploaded_avatar_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(blank=True, default=login_register.models.get_random_avatar, max_length=50, null=True),
        ),
    ]