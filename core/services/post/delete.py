from django import forms
from django.conf import settings
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.api.status_codes import ValidationError401, ValidationError403, ValidationError400, ValidationError404
from apps.users import tasks
from apps.users.models import User
from core.models import Post
from core.services.mixins import ValidationMixin
from core.services.post.get import PostGetService


class PostDeleteService(ValidationMixin, Service):
    user = ModelField(User)
    slug = forms.SlugField(required=True)

    custom_validations = ['_validate_slug']

    def __init__(self):
        super().__init__()
        self.post = None

    def process(self):
        # validate post slug
        self.run_custom_validations()
        self.post = PostGetService.execute({'slug': self.cleaned_data['slug']})
        # send notification
        if self.is_valid():
            self._delete_post()

    def _delete_post(self):
        self.post.state = Post.ModerationStates.ON_DELETION

        task = tasks.delete_post.s(self.post.slug).apply_async(countdown=settings.POST_DELETION_COUNTDOWN)
        self.post.task_id = task.id
        self.post.save()
        return task.id

    def _validate_user(self):
        if not self.cleaned_data['user']:
            raise ValidationError401()
        if not self.cleaned_data['user'] == self.post.author:
            raise ValidationError403()

    def _validate_slug(self):
        try:
            return Post.objects.get(slug=self.cleaned_data['slug'], author=self.cleaned_data['user'])
        except Exception as e:
            if not self.cleaned_data['slug']:
                raise ValidationError400('Missing slug parameter')
            raise ValidationError404('Incorrect slug')
