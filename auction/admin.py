from django.contrib import admin

from .models import Auction, Bid, AuctionHistory, AuctionLike, AuctionCar

# Register your models here.
admin.site.register(Auction)
admin.site.register(AuctionCar)
admin.site.register(Bid)
admin.site.register(AuctionHistory)
admin.site.register(AuctionLike)
