# Generated by Django 5.1.2 on 2024-11-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0005_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
