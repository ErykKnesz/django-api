from django.contrib import admin
from .models import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms

User = get_user_model()

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'user_type')})
UserAdmin.fieldsets = tuple(fields)


admin.site.register(Image)
admin.site.register(User, UserAdmin)