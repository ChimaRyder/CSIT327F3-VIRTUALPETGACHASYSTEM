# Generated by Django 5.1.3 on 2024-11-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_system', '0003_remove_transaction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('WAITING', 'Waiting'), ('SUCCESS', 'Success'), ('DECLINED', 'Declined')], default='WAITING', max_length=20),
        ),
    ]
