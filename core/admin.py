from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Post


class PostAdmin(ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)