# Generated by Django 5.0.7 on 2024-12-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0009_alter_autosmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='autosmodel',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]