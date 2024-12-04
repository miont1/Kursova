from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Auction, Bid
from .forms import AuctionForm
from .utils import paginateAuctions


def allAuctions(request):
    auctions = Auction.objects.filter(is_active=True)
    custom_range, auctions = paginateAuctions(request, auctions, 6)

    context = {'auctions': auctions, 'custom_range': custom_range}
    return render(request, 'auction/all_auctions.html', context)


def auctionDetail(request, auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
        bids = auction.bid_set.all().order_by('-timestamp')

        context = {'auction': auction, 'bids': bids}
        return render(request, 'auctions/auction_detail.html', context)

    except Auction.DoesNotExist:
        return render(request, 'auctions/auction_not_found.html', {'auction_id': auction_id})


@login_required(login_url="login")
def createBid(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        if bid_amount and float(bid_amount) > auction.current_price:
            bid = Bid.objects.create(
                auction=auction,
                user=request.user,
                bid_amount=bid_amount
            )
            auction.current_price = bid_amount
            auction.save()

            messages.success(request, f"Your bid of {bid_amount} was successfully placed!")
            return redirect('auction-detail', auction_id=auction.id)
        else:
            messages.error(request, "Bid amount must be higher than the current price.")

    return redirect('auction-detail', auction_id=auction.id)
