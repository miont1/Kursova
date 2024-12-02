from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import AutosModel
from .forms import AutoForm, CommentAutoForm
from .utils import searchAuto, paginateAutos


# Create your views here.

def all_autos(request):
    autos, search_query = searchAuto(request)
    custom_range, autos = paginateAutos(request, autos, 6)

    context = {'autos': autos, "search_query": search_query, "custom_range": custom_range}
    return render(request, 'autos/all_autos.html', context)


def all_autos_info_number(request, auto_number: int):
    form = CommentAutoForm()
    try:
        auto = AutosModel.objects.get(id=auto_number)
        tags = auto.tags.all()

        if request.method == "POST":
            form = CommentAutoForm(request.POST)
            comment = form.save(commit=False)
            comment.auto = auto
            comment.from_user = request.user.profile

            comment.save()
            auto.getVoteCount

            messages.success(request, "Your comment was successfully submitted!")
            return redirect('single-auto', auto_number=auto.id)

        context = {'auto': auto, 'tags': tags, 'form': form}
        return render(request, 'autos/auto.html', context)

    except AutosModel.DoesNotExist:
        return render(request, 'autos/not-founded.html', {'auto_name': auto_number})


@login_required(login_url="login")
def auto_create(request):
    profile = request.user.profile
    form = AutoForm()
    if request.method == 'POST':
        form = AutoForm(request.POST, request.FILES)
        if form.is_valid():
            auto = form.save(commit=False)
            auto.owner = profile
            auto.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'autos/auto-form.html', context)


@login_required(login_url="login")
def auto_update(request, pk):
    profile = request.user.profile
    auto = profile.autosmodel_set.get(id=pk)
    form = AutoForm(instance=auto)
    if request.method == 'POST':
        form = AutoForm(request.POST, request.FILES, instance=auto)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'autos/auto-form.html', context)


@login_required(login_url="login")
def auto_delete(request, pk):
    profile = request.user.profile
    auto = profile.autosmodel_set.get(id=pk)
    context = {'object': auto}
    if request.method == 'POST':
        auto.delete()
        return redirect('all_autos')
    return render(request, 'delete-template.html', context)
