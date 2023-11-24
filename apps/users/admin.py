from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    # TODO: Add avatar field to CustomUserAdmin
    pass


admin.site.register(User, CustomUserAdmin)