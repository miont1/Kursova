# Generated by Django 5.0.7 on 2024-12-04 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='starting_price',
            new_name='start_price',
        ),
    ]