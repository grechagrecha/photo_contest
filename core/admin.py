from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin

from .models import Post, Like, Comment


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
    actions = ['publish', 'retract', 'recover']

    @admin.action(description='Publish selected posts')
    def publish(self, request, queryset):
        for post in queryset:
            if post.state == Post.ModerationStates.ON_VALIDATION:
                post.publish()
                post.save()
        messages.success(request, 'Posts have been successfully published!')

    @admin.action(description='Retract selected posts')
    def retract(self, request, queryset):
        for post in queryset:
            if post.state == Post.ModerationStates.PUBLISHED:
                post.retract()
                post.save()
        messages.success(request, 'Posts have been successfully retracted!')

    @admin.action(description='Recover selected posts')
    def recover(self, request, queryset):
        for post in queryset:
            if post.state == Post.ModerationStates.ON_DELETION:
                post.recover()
                post.save()
        messages.success(request, 'Posts have been successfully recovered!')


class LikeAdmin(ModelAdmin):
    list_display = [
        'user',
        'post'
    ]


class CommentAdmin(ModelAdmin):
    list_display = [
        'user',
        'post',
        'text'
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
