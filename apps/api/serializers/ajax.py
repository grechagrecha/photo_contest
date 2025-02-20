from rest_framework import serializers

from core.models import Post


class AjaxSearchJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'slug',
            'title',
            'description',
            'number_of_likes',
            'number_of_comments',
            'created_at',
            'author_name',
            'post_url',
            'image_thumbnail_url',
            'like_url'
        ]
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    author_name = serializers.CharField(source='get_author_name')
    post_url = serializers.URLField(source='get_absolute_url')
    image_thumbnail_url = serializers.CharField(source='get_image_thumbnail_url')
    like_url = serializers.URLField(source='get_like_url')
