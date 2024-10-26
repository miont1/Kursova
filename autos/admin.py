from django.contrib import admin

from .models import AutosModel, User, Profile, ProfileComment, AutoComment, Tag
# Register your models here.

admin.site.register(AutosModel)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ProfileComment)
admin.site.register(AutoComment)
admin.site.register(Tag)