from django.db import models
from users.models import Profile
from django.contrib.auth.models import User


# Create your models here.

class AutosModel(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    id = models.BigAutoField(primary_key=True)
    car_brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    featured_image = models.ImageField(null=True, blank=True, default="default-auto.jpg")
    description = models.TextField(null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"


class AutoComment(models.Model):
    VOTE_TYPE = (
        ("like", "Recommend car"),
        ("dislike", "Don't recommend car")
    )
    id = models.BigAutoField(primary_key=True)
    auto = models.ForeignKey(AutosModel, on_delete=models.CASCADE)
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


class Tag(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
