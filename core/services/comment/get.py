from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from service_objects.fields import ModelField
from service_objects.services import Service

from apps.users.models import User
from core.models import Post, Comment
from core.services.mixins import ValidationMixin


class CommentGetService(ValidationMixin, Service):
    slug = forms.SlugField()

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            return self._comment

    @property
    @lru_cache()
    def _comment(self) -> Comment | None:
        try:
            return Comment.objects.get(slug=self.cleaned_data['slug'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
