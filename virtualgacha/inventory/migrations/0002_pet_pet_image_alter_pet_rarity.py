# Generated by Django 5.1.1 on 2024-10-14 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='pet_image',
            field=models.ImageField(blank=True, null=True, upload_to='pets/'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='rarity',
            field=models.IntegerField(choices=[('COMMON', 'Common'), ('UNCOMMON', 'Uncommon'), ('RARE', 'Rare'), ('MYTHICAL', 'Mythical'), ('LEGENDARY', 'Legendary')]),
        ),
    ]
