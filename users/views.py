from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, AdvantageForm, CommentUserForm, MessageForm
from .utils import searchProfile, paginateProfiles


# Create your views here.

def profiles(request):
    profiles, search_query = searchProfile(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    contex = {'profiles': profiles, "search_query": search_query, "custom_range": custom_range}
    return render(request, 'users/profiles.html', contex)


def userProfile(request, pk):
    form = CommentUserForm()
    profile = Profile.objects.get(id=pk)

    adv_descr = profile.advantage_set.exclude(description__exact="").exclude(description__isnull=True)
    adv = profile.advantage_set.filter(description__exact="").union(profile.advantage_set.filter(description__isnull=True))

    if request.method == "POST":
        form = CommentUserForm(request.POST)
        comment = form.save(commit=False)
        comment.profile = profile
        comment.from_user = request.user.profile

        comment.save()
        profile.getVoteCount

        messages.success(request, "Your comment was successfully submitted!")
        return redirect('user-profile', pk=profile.id)

    contex = {'profile': profile, 'adv_descr': adv_descr,
              'adv': adv, "form": form}

    return render(request, 'users/profile.html', contex)


def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unReadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unReadCount': unReadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Your message was sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message-form.html', context)
