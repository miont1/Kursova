from django.db import models
from django.contrib.auth.models import User


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
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = '/static/images/profiles/default-user.png'
        return url

    @property
    def commentators(self):
        querySet = self.profilecomment_set.all().values_list('from_user__id', flat=True)
        return querySet

    @property
    def getVoteCount(self):
        comment = self.profilecomment_set.all()
        upVotes = comment.filter(value="like").count()
        totalVotes = comment.count()
        ratio = (upVotes / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class ProfileComment(models.Model):
    VOTE_TYPE = (
        ("like", "Recommend user"),
        ("dislike", "Don't recommend user")
    )
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments_made", null=True)
    topic = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["from_user", "profile"]]

    def __str__(self):
        return f"{self.from_user} -> {self.profile}"


class Advantage(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['is_read', '-created']
