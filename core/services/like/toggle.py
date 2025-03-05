from functools import lru_cache
from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome

from apps.users.models import User
from core.models import Like, Post
from core.services.post.get import PostGetService


class LikeToggleService(ServiceWithResult):
    slug = forms.SlugField()
    user = ModelField(User)
    
    post = None

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            is_liked = Like.like_toggle(self.cleaned_data['user'], self.cleaned_data['slug'])
            self.post = self._post
            self.result = {
                'liked': is_liked,
                'number_of_likes': self.post.number_of_likes
            }
        return self

    @property
    @lru_cache()
    def _post(self) -> Post:
        outcome = ServiceOutcome(PostGetService, {'post_slug': self.cleaned_data['slug']})
        return outcome.result
