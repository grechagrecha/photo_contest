from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from core.models import Post


class PostGetService(ServiceWithResult):
    """
        Returns a post with a given slug if it exists.
    """
    slug = forms.SlugField()
    post = None

    custom_validations = ['_check_post_presence', ]

    def process(self):
        self.post = self._post
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.post
        return self

    @property
    @lru_cache()
    def _post(self) -> Post | None:
        try:
            return Post.objects.get(slug=self.cleaned_data['slug'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    def _check_post_presence(self):
        if not self.post:
            self.add_error(
                'slug',
                NotFound(
                    message=f'Post with slug = {self.cleaned_data["slug"]} does not exist'
                )
            )
