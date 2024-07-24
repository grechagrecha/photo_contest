from django import forms
from service_objects.services import Service

from core.services.comment.get import CommentGetService
from core.services.mixins import ValidationMixin


class CommentDeleteService(ValidationMixin, Service):
    slug = forms.SlugField()

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self._delete_comment()

    def _delete_comment(self):
        comment = CommentGetService.execute({'slug': self.cleaned_data['slug']})
        if comment:
            comment.delete()
