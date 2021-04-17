from django.contrib import admin
from .models import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class UserImageAdmin(UserAdmin):
    pass


admin.site.register(Image)
admin.site.register(User, UserImageAdmin)