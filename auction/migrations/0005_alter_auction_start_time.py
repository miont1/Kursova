# Generated by Django 5.0.7 on 2024-12-04 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_alter_auction_auto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
