from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from auction.models import Auction


def searchAuction(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    auctions = Auction.objects.distinct().filter(
        Q(auto__car_brand__icontains=search_query) |
        Q(auto__car_model__icontains=search_query) |
        Q(owner__name__icontains=search_query)
    )

    return auctions, search_query


def paginateAuctions(request, auctions, results_per_page):
    page = request.GET.get('page')
    paginator = Paginator(auctions, results_per_page)

    try:
        auctions = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        auctions = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        auctions = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, auctions