from django.conf import settings
from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from apps.api.status_codes import ValidationError404
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
            return self._add_post()

    def _add_post(self) -> Post:
        return Post.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            author=self.cleaned_data['user'],
            image=self.cleaned_data['image']
        )

    def _validate_type(self):
        img_type = self.cleaned_data['image'].content_type.split('/')[1]
        if img_type not in settings.ALLOWED_IMAGE_TYPES:
            raise ValidationError404('Incorrect type of photo')

    def _validate_name(self):
        if Post.objects.filter(title=self.cleaned_data['title']):
            raise ValidationError404('Post with that name already exists')
