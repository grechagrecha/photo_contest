from functools import lru_cache

from django import forms
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome

from apps.users.models import User
from core.models import Comment
from core.services.comment.get import CommentGetService


class CommentDeleteService(ServiceWithResult):
    slug = forms.SlugField()
    user = ModelField(User)
    comment = None

    custom_validations = ['_check_if_user_is_authorized', ]

    def process(self):
        self.comment = self._comment
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_comment()
        return self

    def _delete_comment(self):
        post_slug = self.comment.post.slug
        self.comment.delete()
        return post_slug

    @property
    @lru_cache()
    def _comment(self) -> Comment:
        outcome = ServiceOutcome(CommentGetService, {'slug': self.cleaned_data['slug']})
        return outcome.result

    def _check_if_user_is_authorized(self):
        if self.cleaned_data['user'] != self.comment.user:
            self.add_error(
                'user',
                ValidationError(message=f'User = {self.cleaned_data["user"]} is not authorized to perform this action')
            )
