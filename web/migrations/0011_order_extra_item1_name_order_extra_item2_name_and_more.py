# Generated by Django 5.1.4 on 2025-01-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_alter_order_order_id_alter_wallet_transaction_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='extra_item1_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='extra_item2_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='extra_item3_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='extra_item4_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='thali_type_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='20250104165053', max_length=100),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='transaction_time',
            field=models.CharField(default='20250104165053', max_length=100),
        ),
    ]