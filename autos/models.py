from django.db import models
from users.models import Profile


# Create your models here.

class AutosModel(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    car_brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    featured_image = models.ImageField(null=True, blank=True, default="default-auto.jpg")
    description = models.TextField(null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'car_brand', 'car_model']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/static/images/default-auto.jpg'
        return url

    @property
    def commentators(self):
        querySet = self.autocomment_set.all().values_list('from_user__id', flat=True)
        return querySet

    @property
    def getVoteCount(self):
        comment = self.autocomment_set.all()
        upVotes = comment.filter(value="like").count()
        totalVotes = comment.count()
        ratio = (upVotes / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class AutoComment(models.Model):
    VOTE_TYPE = (
        ("like", "Recommend car"),
        ("dislike", "Don't recommend car")
    )
    id = models.BigAutoField(primary_key=True)
    auto = models.ForeignKey(AutosModel, on_delete=models.CASCADE)
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["from_user", "auto"]]

    def __str__(self):
        return self.topic


class Tag(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name