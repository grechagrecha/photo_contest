from django.conf import settings
from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError

from apps.users.models import User
from core.models import Post


class PostCreateService(ServiceWithResult):
    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()
    user = ModelField(User)

    custom_validations = ['_validate_name', '_validate_type']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self) -> Post:
        return Post.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            author=self.cleaned_data['user'],
            image=self.cleaned_data['image']
        )

    def _validate_type(self):
        img_type = self.cleaned_data['image'].content_type.split('/')[1]
        if img_type not in settings.ALLOWED_IMAGE_TYPES:
            self.add_error(
                'image',
                ValidationError(message=f'Photo with type = "{img_type}" cannot be posted. Please use jpeg')
            )

    def _validate_name(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title):
            self.add_error(
                'title',
                ValidationError(message=f'Post with name = "{title}" already exists')
            )
