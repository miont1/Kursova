from django.contrib import admin
from .models import Profile, ProfileComment, Advantage, Message
# Register your models here.

admin.site.register(Profile)
admin.site.register(ProfileComment)
admin.site.register(Advantage)
admin.site.register(Message)