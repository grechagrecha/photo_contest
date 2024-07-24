from django import forms
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.users.models import User
from core.models import Post, Comment
from core.services.mixins import ValidationMixin


class CommentAddService(ValidationMixin, Service):
    post = ModelField(Post)
    user = ModelField(User)
    text = forms.CharField()

    comment = ModelField(Comment)

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.comment = self._add_comment
        return self.comment

    @property
    def _add_comment(self):
        return Comment.objects.create(
            post=self.cleaned_data['post'],
            user=self.cleaned_data['user'],
            text=self.cleaned_data['text']
        )