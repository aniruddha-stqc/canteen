# Generated by Django 5.1.4 on 2025-01-04 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thali',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=20)),
                ('short_name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('long_name', models.TextField(blank=True)),
            ],
        ),
    ]
