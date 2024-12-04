from django.db import models
from users.models import Profile
from autos.models import AutosModel


class Auction(models.Model):
    id = models.BigAutoField(primary_key=True)
    auto = models.ForeignKey(AutosModel, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

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


class AuctionHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for auction {self.auction.id}"


class AuctionLike(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like for {self.auction} by {self.user}"
