import uuid

from django.db import models
from django_fsm import FSMField, transition


from apps.users.models import User


class Post(models.Model):
    objects = models.Manager()

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
    state = FSMField(default='on_validation')

    # TODO: Comments, votes, thumbnail

    def __str__(self):
        return f'{self.title} by {self.author}'

    @transition(field=state, source='on_validation', target='published')
    def publish(self):
        pass

    @transition(field=state, source='published', target='on_validation')
    def retract(self):
        pass


class Like(models.Model):
    objects = models.Manager()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def like_toggle(cls, user, slug):
        # Think about it
        post = Post.objects.get(slug=slug)
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            like.delete()


class Comment(models.Model):
    objects = models.Manager()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.CharField(max_length=300)

    def __str__(self):
        return f'Comment by {self.user} on {self.post.title}'
