# Generated by Django 5.1.7 on 2025-04-05 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentreadings',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='currentreadings',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]
