from functools import lru_cache

from django import forms
from django.conf import settings
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.errors import ValidationError, NotFound

from apps.users import tasks
from apps.users.models import User
from core.models import Post
from core.services.post.get import PostGetService


class PostDeleteService(ServiceWithResult):
    user = ModelField(User)
    slug = forms.SlugField(required=True)
    post = None

    custom_validations = ['_validate_user', ]

    def process(self):
        self.post = self._post
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_post()
        return self

    def post_process(self):
        self._send_notification()

    def _delete_post(self):
        task = tasks.delete_post.s(self.post.slug).apply_async(countdown=settings.POST_DELETION_COUNTDOWN)
        self.post.remove()
        self.post.task_id = task
        self.post.save()

        return task.id

    # TODO: Implement deletion notifications
    def _send_notification(self):
        pass

    @property
    @lru_cache()
    def _post(self) -> Post:
        outcome = ServiceOutcome(PostGetService, {'slug': self.cleaned_data['slug']})
        return outcome.result

    def _validate_user(self):
        if not self.cleaned_data['user']:
            self.add_error(
                'user',
                NotFound(message=f'User was not provided to the service')
            )
        if not self.cleaned_data['user'] == self.post.author:
            self.add_error(
                'user',
                ValidationError(message=f'Provided user not authorized to perform this action')
            )
