from functools import lru_cache

from django import forms
from django.conf import settings
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome

from apps.users.models import User
from core.models import Post
from core.services.post.get import PostGetService


class PostUpdateService(ServiceWithResult):
    user = ModelField(User)
    slug = forms.SlugField()
    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField(required=False)
    post = None

    custom_validations = ['_check_post_presence', '_validate_author', '_validate_type']

    def process(self):
        self.post = self._post
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_post()
        return self

    def _update_post(self) -> Post:
        # TODO: Extract this to separate validation
        if self.cleaned_data['image']:
            # TODO: Send notification that post was retracted
            self.post.retract()
            self.post.save()

        for key in ['title', 'description', 'image']:
            if self.cleaned_data[key]:
                setattr(self.post, key, self.cleaned_data[key])
        self.post.save()

        return self.post

    def _check_post_presence(self):
        if not self.post:
            self.add_error(
                field='slug',
                error=NotFound(
                    message=f'Post with slug = {self.cleaned_data["slug"]} does not exist'
                )
            )

    def _validate_author(self):
        if not self.cleaned_data['user']:
            self.add_error(
                'user',
                ValidationError(message='User was not specified')
            )
        if not self.cleaned_data['user'] == self.post.author:
            self.add_error(
                'user',
                ValidationError(message='User is not the author')
            )

    def _validate_type(self):
        if self.cleaned_data['image']:
            img_type = self.cleaned_data['image'].content_type.split('/')[1]
            if img_type not in settings.ALLOWED_IMAGE_TYPES:
                self.add_error(
                    'image',
                    ValidationError(message='Incorrect type of photo')
                )

    @property
    @lru_cache()
    def _post(self):
        outcome = ServiceOutcome(PostGetService, {'slug': self.cleaned_data['slug']})
        return outcome.result
