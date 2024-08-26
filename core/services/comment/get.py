from functools import lru_cache

from django import forms
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from core.models import Comment


class CommentGetService(ServiceWithResult):
    slug = forms.SlugField()
    comment = None

    custom_validations = ['_check_comment_presence', ]

    def process(self):
        self.comment = self._comment
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    @lru_cache()
    def _comment(self) -> Comment:
        return Comment.objects.get(slug=self.cleaned_data['slug'])

    def _check_comment_presence(self):
        if not self.comment:
            self.add_error(
                'slug',
                NotFound(message=f'Comment with slug = {self.cleaned_data["slug"]} was not found')
            )
