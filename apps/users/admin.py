from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # TODO: Add avatar field to CustomUserAdmin
    pass


admin.site.register(User, CustomUserAdmin)