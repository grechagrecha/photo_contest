from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    # TODO: Add avatar field to CustomUserAdmin
    list_display = [
        'username',
        'avatar',
        'email',
        'is_staff',
        'is_active'
    ]
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'groups'
    ]
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'username',
                    'avatar'
                ),
            },
        ),
    )
    fieldsets = (
        (None, {'fields': ['password']}),
        ('Personal info',
         {
             'fields': (
                 'username',
                 'email'
             )
         }
         ),
        (
            'Permissions',
            {
                "fields": (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'role'
                ),
            },
        )
    )


admin.site.register(User, CustomUserAdmin)
