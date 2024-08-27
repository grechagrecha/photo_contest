from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from apps.users.models import User
from core.models import Like


class LikeToggleService(ServiceWithResult):
    slug = forms.SlugField()
    user = ModelField(User)

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        self.result = Like.like_toggle(self.cleaned_data['user'], self.cleaned_data['slug'])
        return self
