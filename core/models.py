import uuid

from django.db import models
from django_fsm import FSMField, transition

from apps.users.models import User


class Post(models.Model):
    class ModerationStates(models.TextChoices):
        ON_VALIDATION = 'on_validation', 'On validation'
        PUBLISHED = 'published', 'Published'
        ON_DELETION = 'on_deletion', 'On deletion'

    title = models.CharField(default='post', max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    image = models.ImageField(upload_to='images/posts/')
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    description = models.CharField(default='Empty description.', blank=True, max_length=1000)
    created_at = models.DateTimeField(verbose_name='Date created', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Last updated at', auto_now=True)
    number_of_likes = models.IntegerField(default=0)
    number_of_comments = models.IntegerField(default=0)

    state = FSMField(default=ModerationStates.ON_VALIDATION, choices=ModerationStates.choices)

    objects = models.Manager()

    # TODO: Thumbnail

    def __str__(self):
        return f'{self.title} by {self.author}'

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        self.number_of_likes = Like.objects.filter(post_id=self.pk).count()
        self.number_of_comments = Comment.objects.filter(post_id=self.pk).count()

        super().save()

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
        post.save()


class Comment(models.Model):
    objects = models.Manager()

    slug = models.SlugField(default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
