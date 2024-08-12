from django import forms
from service_objects.services import Service

from core.services.comment.get import CommentGetService


class CommentDeleteService(Service):
    slug = forms.SlugField()

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self._delete_comment()

    def _delete_comment(self):
        comment = CommentGetService.execute({'slug': self.cleaned_data['slug']})
        post_slug = comment.post.slug

        if comment:
            comment.delete()

        return post_slug