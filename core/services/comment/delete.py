from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult, ServiceOutcome

from core.models import Comment
from core.services.comment.get import CommentGetService


class CommentDeleteService(ServiceWithResult):
    slug = forms.SlugField()
    comment = None

    def process(self):
        self.comment = self._comment
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._delete_comment()
        return self

    def _delete_comment(self):
        return self.comment.delete()

    @property
    @lru_cache()
    def _comment(self) -> Comment:
        outcome = ServiceOutcome(CommentGetService, {'slug': self.cleaned_data['slug']})
        return outcome.result
