from functools import lru_cache
from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.api.status_codes import ValidationError401, ValidationError403, ValidationError400, ValidationError404
from apps.users import tasks
from apps.users.models import User
from core.models import Post
from core.services.mixins import ValidationMixin


class PostDeleteService(ValidationMixin, Service):
    user = ModelField(User)
    slug = forms.SlugField(required=True)

    custom_validations = [ '_validate_slug']

    def process(self):
        # validate post slug
        self.run_custom_validations()
        # send notification
        if self.is_valid():
            self._delete_post()

    def _delete_post(self):
        post = self._get_post()
        post.state = Post.ModerationStates.ON_DELETION

        task = tasks.delete_post.s(post.slug).apply_async(countdown=settings.POST_DELETION_COUNTDOWN)
        post.task_id = task.id
        post.save()
        return task.id

    @lru_cache()
    def _get_post(self) -> Post:
        return Post.objects.get(slug=self.cleaned_data['slug'])

    def _validate_user(self):
        if not self.cleaned_data['user']:
            raise ValidationError401()
        if not self.cleaned_data['user'] == self._get_post().author:
            raise ValidationError403()

    def _validate_slug(self):
        try:
            return Post.objects.get(slug=self.cleaned_data['slug'], author=self.cleaned_data['user'])
        except Exception as e:
            if not self.cleaned_data['slug']:
                raise ValidationError400('Missing slug parameter.')
            raise ValidationError404('Incorrect slug')
