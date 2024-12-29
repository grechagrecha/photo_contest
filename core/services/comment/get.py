from functools import lru_cache

from django import forms
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from core.models import Comment


class CommentGetService(ServiceWithResult):
    comment_slug = forms.SlugField()
    comment = None

    custom_validations = [
        '_check_comment_presence',
        '_check_post_presence',
    ]

    def process(self):
        self.comment = self._comment
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    @lru_cache()
    def _comment(self) -> Comment:
        return Comment.objects.get(slug=self.cleaned_data['comment_slug'])

    def _check_post_presence(self):
        if not self.comment.post:
            self.add_error(
                'comment.post',
                ValidationError(
                    message=f'Comment: {self.comment} doesn\'t have a post associated with it'
                )
            )

    def _check_comment_presence(self):
        if not self.comment:
            self.add_error(
                'slug',
                ValidationError(
                    message=f'Comment: {self.comment} was not found'
                )
            )
