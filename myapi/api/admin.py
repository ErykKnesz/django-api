from django.contrib import admin
from .models import Image, Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

'''
fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'user_type')})
UserAdmin.fieldsets = tuple(fields)
'''

admin.site.register(Image)
admin.site.register(Account)
