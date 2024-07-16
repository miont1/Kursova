from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

ALL_MARKS = {
    "AUDI": "Audi AG (German: [ˈaʊ̯di ʔaːˈɡeː]) is a German automotive manufacturer of luxury vehicles headquartered in Ingolstadt, Bavaria, Germany. A subsidiary of the Volkswagen Group, Audi produces vehicles in nine production facilities worldwide.",
    "BMW": "The BMW Group is the world's leading provider of premium cars and motorcycles and the home of the BMW, MINI, Rolls-Royce and BMW Motorrad brands. Our vehicles and products are tailored to the needs of our customers and constantly enhanced – with a clear focus on sustainability and the conservation of resources.",
    "TOYOTA": "Toyota Motor Corp: Overview The company designs, manufactures and sells passenger cars, buses, minivans, trucks, specialty cars, recreational and sport-utility vehicles. It provides financing to dealers and customers for the purchase or lease of vehicles.",
    "LEXUS": "Lexus (レクサス, Rekusasu) is the luxury vehicle division of the Japanese automaker Toyota Motor Corporation. The Lexus brand is marketed in more than 90 countries and territories worldwide[3][6] and is Japan's largest-selling make of premium cars. It has ranked among the 10 largest Japanese global brands in market value.[7] Lexus is headquartered in Nagoya, Japan. Operational centers are located in Brussels, Belgium, and Plano, Texas, United States."
}


def all_autos(request):
    return render(request, 'autos/all_autos.html', {'marks': ALL_MARKS})


def all_autos_info(request, auto_name: str):
    description = ALL_MARKS.get(auto_name)
    context = {'description': description, 'auto_name': auto_name}
    if description:
        return render(request, 'autos/auto.html', context)
    else:
        return render(request, 'autos/not-founded.html', context)


def all_autos_info_number(request, auto_number: int):
    auto_list = list(ALL_MARKS)
    if auto_number > auto_list.__len__():
        return render(request, 'autos/not-founded.html', {'auto_name': auto_number})
    auto = auto_list[auto_number - 1]
    redirect_url = reverse('single-auto', args=(auto,))
    return HttpResponseRedirect(redirect_url)
