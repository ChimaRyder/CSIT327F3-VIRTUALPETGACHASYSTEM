# Generated by Django 5.1.2 on 2024-11-01 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0002_profile_total_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
