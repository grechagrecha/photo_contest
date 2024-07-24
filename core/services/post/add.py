from django import forms
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.api.status_codes import ValidationError404
from apps.users.models import User
from core.models import Post
from core.services.mixins import ValidationMixin


class PostAddService(ValidationMixin, Service):
    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()
    user = ModelField(User)

    custom_validations = ['_validate_name', '_validate_type']

    def __init__(self):
        super().__init__()
        self.post = None

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.post = self._add_post

    @property
    def _add_post(self):
        return Post.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            author=self.cleaned_data['user'],
            image=self.cleaned_data['image']
        )

    def _validate_type(self):
        if self.cleaned_data['image'].content_type.split('/')[1] != 'jpeg':
            raise ValidationError404('Incorrect type of photo')

    def _validate_name(self):
        if Post.objects.filter(title=self.cleaned_data['title']):
            raise ValidationError404('Post with that name already exists')
