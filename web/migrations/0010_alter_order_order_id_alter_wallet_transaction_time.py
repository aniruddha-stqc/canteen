# Generated by Django 5.1.4 on 2025-01-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_order_pay_mode_alter_order_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='20250104162031', max_length=100),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transaction_time',
            field=models.CharField(default='20250104162031', max_length=100),
        ),
    ]
