# Generated by Django 5.0.7 on 2024-11-14 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_advantage_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='short_bio',
            new_name='shortbio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='advantages',
        ),
        migrations.AddField(
            model_name='advantage',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]