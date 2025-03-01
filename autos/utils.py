from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import AutosModel, Tag


def searchAuto(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)

    autos = AutosModel.objects.distinct().filter(
        Q(car_brand__icontains=search_query) |
        Q(car_model__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return autos, search_query


def paginateAutos(request, autos, result):
    page = request.GET.get("page")
    paginator = Paginator(autos, result)
    try:
        autos = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        autos = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        autos = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, autos
