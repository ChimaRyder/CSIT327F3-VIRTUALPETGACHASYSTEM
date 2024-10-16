# Generated by Django 4.2.12 on 2024-10-16 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_pet_rarity'),
        ('lootbox_market', '0002_alter_lootbox_tagged_relevance'),
    ]

    operations = [
        migrations.AddField(
            model_name='lootbox',
            name='drop_table',
            field=models.ManyToManyField(related_name='lootbox_drop_table', to='inventory.pet'),
        ),
        migrations.CreateModel(
            name='LootboxHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_opened', models.DateField(auto_now_add=True)),
                ('user_id', models.IntegerField()),
                ('lootbox_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lootbox_market.lootbox')),
                ('obtained_pets', models.ManyToManyField(related_name='obtained_pets', to='inventory.pet')),
            ],
        ),
    ]
