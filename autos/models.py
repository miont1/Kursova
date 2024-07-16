from django.db import models


# Create your models here.

class AutosModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags', blank=True)

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    def __str__(self):
        return self.username


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200)
    social_links = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ProfileComments(models.Model):
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


class AutoComments(models.Model):
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


class Tags(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
