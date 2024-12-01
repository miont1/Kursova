from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, AdvantageForm


# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    contex = {'profiles': profiles}
    return render(request, 'users/profiles.html', contex)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    adv_descr = profile.advantage_set.exclude(description__exact="").exclude(description__isnull=True)
    adv = profile.advantage_set.filter(description__exact="").union(profile.advantage_set.filter(description__isnull=True))

    contex = {'profile': profile, 'adv_descr': adv_descr,
              'adv': adv}
    return render(request, 'users/profile.html', contex)


def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logget out")
    return redirect('login')


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User was created successfully!")
            login(request, user)
            return redirect("edit-account")
        else:
            messages.error(request, "An error during registration")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile

    advantages = profile.advantage_set.all()

    context = {"profile": profile, 'advantages': advantages}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "users/profile-form.html", context)


@login_required(login_url="login")
def createAdv(request):
    profile = request.user.profile
    form = AdvantageForm()

    if request.method == "POST":
        form = AdvantageForm(request.POST)
        if form.is_valid():
            advantage = form.save(commit=False)
            advantage.owner = profile
            advantage.save()
            messages.success(request, "Advantage was created successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/advantage-form.html", context)


@login_required(login_url="login")
def updateAdv(request, pk):
    profile = request.user.profile
    advantage = profile.advantage_set.get(id=pk)
    form = AdvantageForm(instance=advantage)

    if request.method == "POST":
        form = AdvantageForm(request.POST, instance=advantage)
        if form.is_valid():
            form.save()
            messages.success(request, "Advantage was updated successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/advantage-form.html", context)


@login_required(login_url="login")
def deleteAdv(request, pk):
    profile = request.user.profile
    advantage = profile.advantage_set.get(id=pk)
    if request.method == "POST":
        advantage.delete()
        messages.success(request, "Advantage was deleted successfully!")
        return redirect("account")
    context = {"object": advantage}
    return render(request, "delete-template.html", context)
