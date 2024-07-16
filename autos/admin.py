from django.contrib import admin

from .models import AutosModel, User, Profile, ProfileComments, AutoComments, Tags
# Register your models here.

admin.site.register(AutosModel)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ProfileComments)
admin.site.register(AutoComments)
admin.site.register(Tags)