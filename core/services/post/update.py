from django import forms
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.api.status_codes import ValidationError401, ValidationError403
from apps.users.models import User
from core.models import Post
from core.services.mixins import ValidationMixin
from core.services.post.get import PostGetService


class PostUpdateService(ValidationMixin, Service):
    user = ModelField(User)

    slug = forms.SlugField()
    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField(required=False)

    custom_validations = ['_validate_author']

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
