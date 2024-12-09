import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, AdvantageForm, CommentUserForm, MessageForm
from .utils import searchProfile, paginateProfiles

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def profiles(request):
    logger.info("Відкрито сторінку профілів.")
    profiles, search_query = searchProfile(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    logger.info(f"Пошук профілів завершено. Кількість знайдених: {len(profiles)}.")
    contex = {'profiles': profiles, "search_query": search_query, "custom_range": custom_range}
    return render(request, 'users/profiles.html', contex)


def userProfile(request, pk):
    logger.info(f"Відкрито профіль користувача з ID: {pk}.")
    form = CommentUserForm()
    profile = Profile.objects.get(id=pk)

    adv_descr = profile.advantage_set.exclude(description__exact="").exclude(description__isnull=True)
    adv = profile.advantage_set.filter(description__exact="").union(profile.advantage_set.filter(description__isnull=True))

    if request.method == "POST":
        logger.info(f"Отримано POST-запит на додавання коментаря до профілю {profile.id}.")
        form = CommentUserForm(request.POST)
        comment = form.save(commit=False)
        comment.profile = profile
        comment.from_user = request.user.profile
        comment.save()
        profile.getVoteCount
        logger.info(f"Коментар успішно збережено для профілю {profile.id}.")
        messages.success(request, "Your comment was successfully submitted!")
        return redirect('user-profile', pk=profile.id)

    contex = {'profile': profile, 'adv_descr': adv_descr, 'adv': adv, "form": form}
    return render(request, 'users/profile.html', contex)


def loginUser(request):
    logger.info("Користувач відкрив форму логіну.")
    if request.user.is_authenticated:
        logger.info("Користувач вже аутентифікований, перенаправлення на сторінку профілів.")
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.error(f"Користувач з ім'ям {username} не знайдений.")
            messages.error(request, "username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.info(f"Користувач {username} успішно увійшов.")
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            logger.error("Невірне ім'я користувача або пароль.")
            messages.error(request, "Username OR password is incorrect")

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logger.info(f"Користувач {request.user.username} вийшов з акаунту.")
    logout(request)
    messages.info(request, "User was logged out")
    return redirect('login')


def registerUser(request):
    logger.info("Користувач відкрив форму реєстрації.")
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            logger.info(f"Користувач {user.username} успішно зареєстрований.")
            messages.success(request, "User was created successfully!")
            login(request, user)
            return redirect("edit-account")
        else:
            logger.warning("Помилка при реєстрації користувача.")
            messages.error(request, "An error during registration")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def userAccount(request):
    logger.info(f"Користувач {request.user.username} відкрив свій акаунт.")
    profile = request.user.profile
    advantages = profile.advantage_set.all()
    context = {"profile": profile, 'advantages': advantages}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    logger.info(f"Користувач {request.user.username} відкрив форму редагування профілю.")
    form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save()
            logger.info(f"Профіль користувача {request.user.username} успішно оновлено.")
            return redirect("account")
        else:
            logger.warning("Форма редагування профілю не пройшла валідацію.")
    context = {"form": form}
    return render(request, "users/profile-form.html", context)


@login_required(login_url="login")
def createAdv(request):
    logger.info(f"Користувач {request.user.username} відкрив форму для створення переваги.")
    profile = request.user.profile
    form = AdvantageForm()

    if request.method == "POST":
        form = AdvantageForm(request.POST)
        if form.is_valid():
            advantage = form.save(commit=False)
            advantage.owner = profile
            advantage.save()
            logger.info(f"Перевага {advantage} успішно створена користувачем {request.user.username}.")
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
            logger.info(f"Перевага {advantage} успішно оновлена користувачем {request.user.username}.")
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
        logger.info(f"Перевага {advantage} успішно видалена користувачем {request.user.username}.")
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
