# Generated by Django 5.1.4 on 2025-01-04 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_order_order_id_alter_wallet_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_mode',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='20250104160646', max_length=100),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transaction_time',
            field=models.CharField(default='20250104160646', max_length=100),
        ),
    ]
