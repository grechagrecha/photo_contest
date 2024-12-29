from functools import lru_cache

from django import forms
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome

from apps.users.models import User
from core.models import Comment
from core.services.comment.get import CommentGetService


class CommentReplyService(ServiceWithResult):
    user = ModelField(User)
    comment_slug = forms.SlugField()
    text = forms.CharField()
    post = None

    custom_validations = [
        '_check_if_user_logged_in',
        '_check_if_text_empty',
    ]

    def process(self):
        self.parent_comment = self._parent_comment
        self.post = self._post
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_comment()
            self.post.save()
        return self

    def _create_comment(self):
        return Comment.objects.create(
            post=self.post,
            parent_comment=self.parent_comment,
            user=self.cleaned_data['user'],
            text=self.cleaned_data['text']
        )

    @property
    @lru_cache()
    def _post(self):
        return self.parent_comment.post

    @property
    @lru_cache()
    def _parent_comment(self):
        outcome = ServiceOutcome(
            CommentGetService,
            {'slug': self.cleaned_data['comment_slug']}
        )
        return outcome.result

    def _check_if_user_logged_in(self):
        if not self.cleaned_data['user'].is_authenticated:
            self.add_error(
                'user',
                ValidationError(message='User is not authenticated')
            )

    def _check_if_text_empty(self):
        if self.cleaned_data['text'].strip() == '':
            self.add_error(
                'text',
                ValidationError(message='Comment text is empty')
            )
