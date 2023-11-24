import uuid

from django.db import models

from apps.users.models import User


class Post(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(default='post', max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/posts/')
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    description = models.CharField(
        default='There should have been a description, but it was not filled.',
        blank=True,
        max_length=1000
    )
    # TODO: Comments, votes, thumbnail
