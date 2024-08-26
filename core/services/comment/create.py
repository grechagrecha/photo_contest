from django import forms
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from apps.users.models import User
from core.models import Post, Comment


class CommentAddService(ServiceWithResult):
    post = ModelField(Post)
    user = ModelField(User)
    text = forms.CharField()

    custom_validations = ['_check_if_user_logged_in', '_check_if_text_empty']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_comment()
        return self

    def _create_comment(self):
        return Comment.objects.create(
            post=self.cleaned_data['post'],
            user=self.cleaned_data['user'],
            text=self.cleaned_data['text']
        )

    def _check_if_user_logged_in(self):
        if not self.cleaned_data['user'].is_authenticated:
            self.add_error(
                'user',
                ValidationError(message=f'User is not authenticated')
            )

    def _check_if_text_empty(self):
        if self.cleaned_data['text'].strip() == '':
            self.add_error(
                'text',
                ValidationError(message=f'Comment text is empty')
            )

    def _check_post_presence(self):
        if not self.cleaned_data['post']:
            self.add_error(
                'post',
                ValidationError(message=f'Post was not provided')
            )
