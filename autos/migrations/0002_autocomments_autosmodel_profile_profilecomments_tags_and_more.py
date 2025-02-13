# Generated by Django 5.0.7 on 2024-10-01 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoComments',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=30)),
                ('comment', models.TextField()),
                ('value', models.CharField(choices=[('like', 'Recommend car'), ('dislike', "Don't recommend car")], max_length=200)),
                ('vote_total', models.IntegerField(blank=True, default=0, null=True)),
                ('vote_ratio', models.IntegerField(blank=True, default=0, null=True)),
                ('views', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AutosModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('car_brand', models.CharField(max_length=50)),
                ('car_model', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('demo_link', models.CharField(blank=True, max_length=2000, null=True)),
                ('source_link', models.CharField(blank=True, max_length=2000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True, null=True)),
                ('location', models.CharField(max_length=200)),
                ('social_links', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(upload_to='profile_images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileComments',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=30)),
                ('comment', models.TextField()),
                ('value', models.CharField(choices=[('like', 'Recommend profile'), ('dislike', "Don't recommend profile")], max_length=200)),
                ('vote_total', models.IntegerField(blank=True, default=0, null=True)),
                ('vote_ratio', models.IntegerField(blank=True, default=0, null=True)),
                ('views', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autos.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=25)),
                ('second_name', models.CharField(max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.DeleteModel(
            name='autos_model',
        ),
        migrations.AddField(
            model_name='autocomments',
            name='auto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autos.autosmodel'),
        ),
        migrations.AddField(
            model_name='autosmodel',
            name='tags',
            field=models.ManyToManyField(blank=True, to='autos.tags'),
        ),
        migrations.AddField(
            model_name='profilecomments',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autos.user'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autos.user'),
        ),
        migrations.AddField(
            model_name='autocomments',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autos.user'),
        ),
    ]
