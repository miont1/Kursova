from django.contrib.auth.models import User
from .models import Profile

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        subject = 'Welcome to AutoShop'
        message = 'We are glad you choose us!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


def updateUsers(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUsers, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
