import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import AutosModel, Tag
from .forms import AutoForm, CommentAutoForm
from .utils import searchAuto, paginateAutos

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def all_autos(request):
    logger.info("Відкрито сторінку всіх авто.")
    autos, search_query = searchAuto(request)
    custom_range, autos = paginateAutos(request, autos, 6)
    logger.info(f"Пошук авто завершено. Кількість знайдених: {len(autos)}.")
    context = {'autos': autos, "search_query": search_query, "custom_range": custom_range}
    return render(request, 'autos/all_autos.html', context)


def all_autos_info_number(request, auto_number: int):
    logger.info(f"Відкрито сторінку авто з ID: {auto_number}.")
    form = CommentAutoForm()
    try:
        auto = AutosModel.objects.get(id=auto_number)
        tags = auto.tags.all()
        logger.info(f"Знайдено авто: {auto}. Кількість тегів: {tags.count()}.")

        if request.method == "POST":
            logger.info("Отримано POST-запит на додавання коментаря.")
            form = CommentAutoForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.auto = auto
                comment.from_user = request.user.profile
                comment.save()
                auto.getVoteCount
                logger.info("Коментар успішно збережено.")
                messages.success(request, "Your comment was successfully submitted!")
                return redirect('single-auto', auto_number=auto.id)
            else:
                logger.warning("Форма коментаря не пройшла валідацію.")

        context = {'auto': auto, 'tags': tags, 'form': form}
        return render(request, 'autos/auto.html', context)

    except AutosModel.DoesNotExist:
        logger.error(f"Авто з ID {auto_number} не знайдено.")
        return render(request, 'autos/not-founded.html', {'auto_name': auto_number})


@login_required(login_url="login")
def auto_create(request):
    profile = request.user.profile
    logger.info(f"Користувач {profile} відкрив форму створення авто.")
    form = AutoForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        logger.info(f"Отримано POST-запит на створення авто від користувача {profile}.")
        form = AutoForm(request.POST, request.FILES)
        if form.is_valid():
            auto = form.save(commit=False)
            auto.owner = profile
            auto.save()
            logger.info(f"Авто успішно створено: {auto}.")
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                auto.tags.add(tag)
            return redirect('account')

        else:
            logger.warning("Форма створення авто не пройшла валідацію.")
    context = {'form': form}
    return render(request, 'autos/auto-form.html', context)


@login_required(login_url="login")
def auto_update(request, pk):
    profile = request.user.profile
    logger.info(f"Користувач {profile} відкрив форму редагування авто з ID: {pk}.")
    auto = profile.autosmodel_set.get(id=pk)
    form = AutoForm(instance=auto)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        logger.info(f"Отримано POST-запит на оновлення авто з ID: {pk}.")
        form = AutoForm(request.POST, request.FILES, instance=auto)
        if form.is_valid():
            auto.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                auto.tags.add(tag)
            logger.info(f"Авто з ID {pk} успішно оновлено.")
            return redirect('account')
        else:
            logger.warning("Форма оновлення авто не пройшла валідацію.")

    context = {'form': form, 'auto': auto}
    return render(request, 'autos/auto-form.html', context)


@login_required(login_url="login")
def auto_delete(request, pk):
    profile = request.user.profile
    logger.info(f"Користувач {profile} відкрив форму видалення авто з ID: {pk}.")
    auto = profile.autosmodel_set.get(id=pk)
    context = {'object': auto}
    if request.method == 'POST':
        logger.info(f"Отримано POST-запит на видалення авто з ID: {pk}.")
        auto.delete()
        logger.info(f"Авто з ID {pk} успішно видалено.")
        return redirect('account')
    return render(request, 'delete-template.html', context)
