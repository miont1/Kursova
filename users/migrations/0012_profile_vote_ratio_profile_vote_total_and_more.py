# Generated by Django 5.0.7 on 2024-12-02 21:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profilecomment_from_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='vote_ratio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='vote_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='profilecomment',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_made', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='profilecomment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AlterField(
            model_name='profilecomment',
            name='value',
            field=models.CharField(choices=[('like', 'Recommend user'), ('dislike', "Don't recommend user")], max_length=200),
        ),
    ]
