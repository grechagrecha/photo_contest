from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin

from .models import Post, Like


class PostAdmin(ModelAdmin):
    list_display = [
        'title',
        'image',
        'author',
        'created_at',
        'updated_at',
        'state'
    ]
    list_filter = [
        'author',
        'state',
    ]
    actions = ['publish', 'retract']

    @admin.action(description='Publish selected posts')
    def publish(self, request, queryset):
        for post in queryset:
            if post.state == 'on_validation':
                post.publish()
                post.save()
        messages.success(request, 'Posts have been successfully published!')

    @admin.action(description='Retract selected posts')
    def retract(self, request, queryset):
        for post in queryset:
            if post.state == 'published':
                post.retract()
                post.save()
        messages.success(request, 'Posts have been successfully retracted!')


class LikeAdmin(ModelAdmin):
    list_display = [
        'user',
        'post'
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
