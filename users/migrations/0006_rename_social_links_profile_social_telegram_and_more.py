# Generated by Django 5.0.7 on 2024-11-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_short_bio_profile_shortbio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='social_links',
            new_name='social_telegram',
        ),
        migrations.AddField(
            model_name='profile',
            name='social_youtube',
            field=models.TextField(blank=True, null=True),
        ),
    ]