from django.contrib import admin

from .models import AutosModel, AutoComment, Tag
# Register your models here.

admin.site.register(AutosModel)
admin.site.register(AutoComment)
admin.site.register(Tag)