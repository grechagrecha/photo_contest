from django import forms
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.users.models import User
from core.models import Post, Comment


class CommentAddService(Service):
    post = ModelField(Post)
    user = ModelField(User)
    text = forms.CharField()

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            return self._add_comment()

    def _add_comment(self):
        return Comment.objects.create(
            post=self.cleaned_data['post'],
            user=self.cleaned_data['user'],
            text=self.cleaned_data['text']
        )