# Generated by Django 5.1.4 on 2025-01-04 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_customer_extra'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='long_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='wallet_id',
        ),
    ]
