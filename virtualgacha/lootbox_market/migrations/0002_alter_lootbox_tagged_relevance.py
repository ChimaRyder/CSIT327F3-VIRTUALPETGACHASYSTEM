# Generated by Django 4.2.12 on 2024-10-02 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lootbox_market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lootbox',
            name='tagged_relevance',
            field=models.CharField(choices=[('popular', 'Popular'), ('recent', 'Recent'), ('featured', 'Featured')], default='recent', max_length=10),
        ),
    ]
