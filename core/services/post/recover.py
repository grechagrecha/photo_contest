from functools import lru_cache

from django import forms
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome

from apps.users.models import User
from core.celery import app
from core.models import Post
from core.services.post.get import PostGetService


class PostRecoverService(ServiceWithResult):
    slug = forms.SlugField()
    user = ModelField(User)
    post = None

    custom_validations = ['_check_if_post_on_deletion', '_validate_author', ]

    def process(self):
        self.post = self._post
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._recover_post()
        return self

    def _recover_post(self):
        app.control.revoke(self.post.task_id)
        self.post.recover()
        self.post.save()
        return self.post

    @property
    @lru_cache()
    def _post(self) -> Post:
        outcome = ServiceOutcome(PostGetService, {'slug': self.cleaned_data['slug']})
        return outcome.result

    def _validate_author(self):
        if self.post.author != self.cleaned_data['user']:
            self.add_error(
                'user',
                ValidationError(message=f'You are not authorized to perform this action')
            )

    def _check_if_post_on_deletion(self):
        if self.post.state != Post.ModerationStates.ON_DELETION:
            self.add_error(
                'state',
                ValidationError(message=f'Post {self.post} is not on deletion')
            )
