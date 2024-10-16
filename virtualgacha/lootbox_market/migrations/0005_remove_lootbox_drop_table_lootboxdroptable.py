# Generated by Django 4.2.12 on 2024-10-16 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_pet_rarity'),
        ('lootbox_market', '0004_rename_history_id_lootboxhistory_lootbox_history_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lootbox',
            name='drop_table',
        ),
        migrations.CreateModel(
            name='LootboxDropTable',
            fields=[
                ('lootbox_drop_table_id', models.AutoField(primary_key=True, serialize=False)),
                ('drop_rate', models.IntegerField()),
                ('lootbox_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lootbox_market.lootbox')),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.pet')),
            ],
        ),
    ]
