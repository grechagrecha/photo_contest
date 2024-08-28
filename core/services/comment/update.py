from functools import lru_cache

from django import forms
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome

from apps.users.models import User
from core.models import Comment
from core.services.comment.get import CommentGetService


class CommentUpdateService(ServiceWithResult):
    slug = forms.SlugField()
    text = forms.CharField()
    user = ModelField(User)
    comment = None

    custom_validations = ['_check_comment_presence', '_check_if_user_is_authorized']

    def process(self):
        self.comment = self._comment
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_comment()
        return self

    def _update_comment(self) -> Comment:
        self.comment.text = self.cleaned_data['text']
        self.comment.save()
        return self.comment

    @property
    @lru_cache()
    def _comment(self) -> Comment:
        outcome = ServiceOutcome(CommentGetService, {'slug': self.cleaned_data['slug']})
        return outcome.result

    def _check_if_user_is_authorized(self):
        if self.cleaned_data['user'] != self.comment.user:
            self.add_error(
                'user',
                ValidationError(message=f'User = {self.cleaned_data['user']} is not authorized to perform this action')
            )

    def _check_comment_presence(self):
        if not self.comment:
            self.add_error(
                'slug',
                NotFound(message=f'Comment with slug = {self.cleaned_data["slug"]} was not found')
            )
