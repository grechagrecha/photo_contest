from django import forms
from django.db.models import Q
from service_objects.services import ServiceWithResult

from core.models import Post


class AjaxSearchService(ServiceWithResult):
    search_query = forms.CharField(required=False)
    posts = None

    custom_validations = []

    def process(self):
        self.posts = self._post_search
        if self.is_valid():
            self.result = self.posts
        return self

    @property
    def _post_search(self):
        posts = Post.objects.filter(
            Q(state=Post.ModerationStates.PUBLISHED) |
            Q(state=Post.ModerationStates.ON_DELETION)
        )

        if self.cleaned_data['search_query']:
            posts = posts.filter(
                Q(title__icontains=self.cleaned_data['search_query']) |
                Q(description__icontains=self.cleaned_data['search_query']) |
                Q(author__username__icontains=self.cleaned_data['search_query']))
        return posts
