# Generated by Django 5.0.7 on 2024-12-02 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilecomment',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
        migrations.AlterField(
            model_name='profilecomment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_comments', to='users.profile'),
        ),
        migrations.AlterUniqueTogether(
            name='profilecomment',
            unique_together={('from_user', 'profile')},
        ),
    ]