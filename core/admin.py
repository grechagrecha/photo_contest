from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Post


class PostAdmin(ModelAdmin):
    list_display = [
        'title',
        'image',
        'author',
        'created_at',
        'updated_at'
    ]
    list_filter = [
        'author'
    ]


admin.site.register(Post, PostAdmin)
