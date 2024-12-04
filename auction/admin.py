from django.contrib import admin

from .models import Auction, Bid, AuctionHistory, AuctionLike

# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(AuctionHistory)
admin.site.register(AuctionLike)
