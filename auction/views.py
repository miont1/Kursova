import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from users.models import Profile
from .models import Auction, AuctionLike
from .forms import CreateAuctionForm, AuctionCarForm, BidForm
from .utils import paginateAuctions, searchAuction


def allAuctions(request):
    auctions, search_query = searchAuction(request)
    custom_range, auctions = paginateAuctions(request, auctions, 6)

    context = {'auctions': auctions, 'custom_range': custom_range, "search_query": search_query}
    return render(request, 'auction/all_auctions.html', context)


def singleAuction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    user = request.user.profile

    initial_liked = auction.auctionlike_set.filter(user=user).exists()

    # Логіка для додавання/видалення лайка
    if request.method == 'POST':
        if 'like' in request.POST:
            if initial_liked:
                # Якщо лайк вже є, видалити його
                auction.auctionlike_set.filter(user=user).delete()
                auction.like_count -= 1
            else:
                # Якщо лайка немає, додати новий
                AuctionLike.objects.create(auction=auction, user=user)
                auction.like_count += 1
            auction.save()

        # Логіка для ставлення ставки
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data['bid_amount']
            if bid_amount > auction.current_price:
                auction.current_price = bid_amount
                auction.save()
                messages.success(request, "You successfully updated bid!")
                return redirect('single-auction', auction_id=auction.id)
            else:
                messages.error(request, "Your bid needs to be bigger than current price!")

    context = {
        'auction': auction,
        'bid_form': BidForm(),
        'initial_liked': initial_liked,
    }

    return render(request, 'auction/single_auction.html', context)


@login_required(login_url="login")
def auctionCreate(request):
    profile = request.user.profile
    car_form = AuctionCarForm()
    auction_form = CreateAuctionForm()

    if request.method == 'POST':
        car_form = AuctionCarForm(request.POST, request.FILES)
        auction_form = CreateAuctionForm(request.POST)
        if car_form.is_valid() and auction_form.is_valid():
            auction_car = car_form.save(commit=False)
            auction_car.owner = profile
            auction_car.save()

            auction = auction_form.save(commit=False)
            auction.auto = auction_car
            auction.owner = profile
            auction.current_price = auction.start_price
            auction.save()
            messages.success(request, "You successfully created Auction!")
            return redirect('all_auctions')

    context = {'car_form': car_form, 'auction_form': auction_form}
    return render(request, 'auction/auction-form.html', context)


@login_required(login_url="login")
def auctionUpdate(request, auction_id):
    profile = request.user.profile
    auction = profile.auction_set.get(id=auction_id)
    car_form = AuctionCarForm(instance=auction.auto)
    auction_form = CreateAuctionForm(instance=auction)

    if request.method == 'POST':
        car_form = AuctionCarForm(request.POST, request.FILES, instance=auction.auto)
        auction_form = CreateAuctionForm(request.POST, instance=auction)

        if car_form.is_valid() and auction_form.is_valid():
            car_form.save()
            auction_form.save()
            messages.info(request, "You successfully updated Auction!")
            return redirect('account')

    context = {'car_form': car_form, 'auction_form': auction_form, 'auction': auction}
    return render(request, 'auction/auction-form.html', context)


@login_required(login_url="login")
def auctionDelete(request, auction_id):
    profile = request.user.profile
    auction = profile.auction_set.get(id=auction_id)
    context = {'object': auction}

    if request.method == 'POST':
        auction.delete()
        messages.info(request, "Auction was  successfully deleted!")
        return redirect('account')

    return render(request, 'delete-template.html', context)


@csrf_exempt
def like_auction(request, auction_id):
    if request.method == 'POST':
        # Отримуємо дані з тіла запиту
        data = json.loads(request.body)
        liked = data.get('liked')

        try:
            # Знаходимо аукціон за ID
            auction = Auction.objects.get(id=auction_id)

            # Логіка для лайків (як приклад, можна змінювати поле like_count)
            if liked:
                auction.like_count += 1
            else:
                auction.like_count -= 1
            auction.save()

            return JsonResponse({'status': 'success', 'like_count': auction.like_count})

        except Auction.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Auction not found'}, status=404)

    return JsonResponse({'status': 'error'}, status=405)
