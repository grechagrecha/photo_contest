import uuid

from django.db import models
from django.utils import timezone

from apps.users.models import User


class Post(models.Model):
    title = models.CharField(default='post', max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    image = models.ImageField(upload_to='images/posts/')
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(verbose_name='Date created', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Last updated at', auto_now=True)
    description = models.CharField(
        default='There should have been a description, but it was not filled.',
        blank=True,
        max_length=1000,
    )

    # TODO: Comments, votes, thumbnail

    def __str__(self):
        return self.title
