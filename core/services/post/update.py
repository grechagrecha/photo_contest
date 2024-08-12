from django import forms
from django.conf import settings
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from apps.api.status_codes import ValidationError401, ValidationError403, ValidationError404
from apps.users.models import User
from core.models import Post
from core.services.post.get import PostGetService


class PostUpdateService(ServiceWithResult):
    user = ModelField(User)

    slug = forms.SlugField()
    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField(required=False)

    custom_validations = ['_validate_author', '_validate_type']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            return self._update_post()

    def _update_post(self) -> Post:
        post = PostGetService.execute({'slug': self.cleaned_data['slug']})

        for key in ['title', 'description', 'image']:
            if self.cleaned_data[key]:
                setattr(post, key, self.cleaned_data[key])
        post.save()

        return post

    def _validate_author(self):
        post = PostGetService.execute({'slug': self.cleaned_data['slug']})
        if not self.cleaned_data['user']:
            raise ValidationError401()
        if not self.cleaned_data['user'] == post.author:
            raise ValidationError403()

    def _validate_type(self):
        img_type = self.cleaned_data['image'].content_type.split('/')[1]
        if img_type not in settings.ALLOWED_IMAGE_TYPES:
            raise ValidationError404('Incorrect type of photo')
