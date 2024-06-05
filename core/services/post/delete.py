from functools import lru_cache

from django import forms
from django.http import HttpResponse
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.users import tasks
from apps.users.models import User
from core.models import Post


class PostDeleteService(Service):
    user = ModelField(User)
    slug = forms.SlugField(required=False)

    def process(self):
        # validate user and post slug
        # send notification
        if not self.is_valid():
            return

        if not self._validate_user():
            return HttpResponse('Unauthorized', status=401)

        return self._delete_post()

    def _delete_post(self):
        post = self._get_post()
        post.state = Post.ModerationStates.ON_DELETION
        task = tasks.delete_post.s(post.slug).apply_async(countdown=20)
        post.task_id = task.id
        post.save()
        return task.id

    @lru_cache()
    def _get_post(self) -> Post:
        return Post.objects.get(slug=self.cleaned_data['slug'])

    def _validate_user(self):
        # TODO: Change that!
        return self.cleaned_data['user'] == self._get_post().author
