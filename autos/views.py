from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


# Create your views here.


def all_autos(request):
    return HttpResponse("все машины")


ALL_MARKS = {
    "AUDI": "Audi AG (German: [ˈaʊ̯di ʔaːˈɡeː]) is a German automotive manufacturer of luxury vehicles headquartered in Ingolstadt, Bavaria, Germany. A subsidiary of the Volkswagen Group, Audi produces vehicles in nine production facilities worldwide.",
    "BMW": "The BMW Group is the world's leading provider of premium cars and motorcycles and the home of the BMW, MINI, Rolls-Royce and BMW Motorrad brands. Our vehicles and products are tailored to the needs of our customers and constantly enhanced – with a clear focus on sustainability and the conservation of resources.",
    "TOYOTA": "Toyota Motor Corp: Overview The company designs, manufactures and sells passenger cars, buses, minivans, trucks, specialty cars, recreational and sport-utility vehicles. It provides financing to dealers and customers for the purchase or lease of vehicles."
}


def all_autos_info(request, auto_name: str):
    description = ALL_MARKS.get(auto_name)
    if description:
        return HttpResponse(description)
    else:
        return HttpResponseNotFound(f"Auto not founded {auto_name}")


def all_autos_info_number(request, auto_name: int):
    auto_list = list(ALL_MARKS)
    if auto_name > auto_list.__len__():
        return HttpResponseNotFound(f"Auto number not founded {auto_name}")
    auto = auto_list[auto_name - 1]
    redirect_url = reverse('auto-name', args=(auto, ))
    return HttpResponseRedirect(redirect_url)
