from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, default="default@example.com")
    username = models.CharField(max_length=50, null=True, blank=True)
    shortbio = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, default="profiles/default-user.png", upload_to='profiles/')
    location = models.CharField(max_length=200)
    social_telegram = models.CharField(max_length=500, null=True, blank=True)
    social_youtube = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class ProfileComment(models.Model):
    VOTE_TYPE = (
        ("like", "Recommend profile"),
        ("dislike", "Don't recommend profile")
    )
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=30)
    comment = models.TextField()
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic


class Advantage(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
