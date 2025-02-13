from django.db import models
from users.models import Profile


class AuctionCar(models.Model):
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True, default="default-auto.jpg")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car_brand} {self.car_model} (Auction)"


class Auction(models.Model):
    id = models.BigAutoField(primary_key=True)
    auto = models.ForeignKey(AuctionCar, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True, editable=True)
    end_time = models.DateTimeField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def update_like_count(self):
        self.like_count = AuctionLike.objects.filter(auction=self).count()
        self.save()

    def __str__(self):
        return f"Auction for {self.auto} by {self.owner}"


class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.user} for {self.auction.auto}"


class AuctionLike(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like for {self.auction} by {self.user}"
