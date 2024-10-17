# Generated by Django 5.1.1 on 2024-10-16 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_pet_rarity'),
        ('lootbox_market', '0006_remove_lootboxdroptable_drop_rate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pull',
            fields=[
                ('pull_id', models.AutoField(primary_key=True, serialize=False)),
                ('roll_info', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('lootbox_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lootbox_market.lootbox')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PullPet',
            fields=[
                ('pull_pet_id', models.AutoField(primary_key=True, serialize=False)),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.pet')),
                ('pull_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lootbox_market.pull')),
            ],
        ),
    ]
