from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import AutosModel
from .forms import AutoForm

# Create your views here.

def all_autos(request):
    autos = AutosModel.objects.all()
    context = {'autos': autos}
    return render(request, 'autos/all_autos.html', context)


def all_autos_info(request, auto_name: str):
    try:
        auto = AutosModel.objects.get(car_brand=auto_name)
        tags = auto.tags.all()
        context = {'auto': auto, 'tags': tags}
        return render(request, 'autos/auto.html', context)
    except AutosModel.DoesNotExist:
        return render(request, 'autos/not-founded.html', {'auto_name': auto_name})


def all_autos_info_number(request, auto_number: int):
    try:
        auto = AutosModel.objects.get(id=auto_number)  # Виклик get() всередині try
        redirect_url = reverse('single-auto', args=(auto.car_brand,))
        return HttpResponseRedirect(redirect_url)
    except AutosModel.DoesNotExist:
        return render(request, 'autos/not-founded.html', {'auto_name': auto_number})


def auto_create(request):
    form = AutoForm()
    if request.method == 'POST':
        form = AutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_autos')
    context = {'form': form}
    return render(request, 'autos/auto-form.html', context)


def auto_update(request, pk):
    auto = AutosModel.objects.get(id=pk)
    form = AutoForm(instance=auto)
    if request.method == 'POST':
        form = AutoForm(request.POST, instance=auto)
        if form.is_valid():
            form.save()
            return redirect('all_autos')
    context = {'form': form}
    return render(request, 'autos/auto-form.html', context)

def auto_delete(request, pk):
    auto = AutosModel.objects.get(id=pk)
    context = {'object': auto}
    if request.method == 'POST':
        auto.delete()
        return redirect('all_autos')
    return render(request, 'autos/delete-template.html', context)
