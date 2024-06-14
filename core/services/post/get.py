from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from service_objects.services import Service

from core.models import Post
from core.services.mixins import ValidationMixin


class PostGetService(ValidationMixin, Service):
    """
        Returns a post with a given slug if it exists, else returns None.
    """
    slug = forms.SlugField()

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            return self._post

    @property
    @lru_cache()
    def _post(self) -> Post | None:
        try:
            return Post.objects.get(slug=self.cleaned_data['slug'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
