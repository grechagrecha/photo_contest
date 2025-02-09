from django import forms
from django.db.models import Q
from service_objects.services import ServiceWithResult

from core.models import Post


class AjaxSearchService(ServiceWithResult):
    search_query = forms.CharField(required=False)
    sort_order = forms.CharField(required=False)
    posts = None

    custom_validations = []

    def process(self):
        self.posts = self._post_search_and_sort
        if self.is_valid():
            self.result = self.posts
        return self

    @property
    def _post_search_and_sort(self):
        sort_order = self.cleaned_data['sort_order'] or 'recent'

        posts = Post.objects.filter(
            Q(state=Post.ModerationStates.PUBLISHED) |
            Q(state=Post.ModerationStates.ON_DELETION)
        )

        if self.cleaned_data['search_query']:
            posts = posts.filter(
                Q(title__icontains=self.cleaned_data['search_query']) |
                Q(description__icontains=self.cleaned_data['search_query']) |
                Q(author__username__icontains=self.cleaned_data['search_query']))

        match sort_order:
            case 'recent':
                posts = posts.order_by('-created_at')
            case 'liked':
                posts = posts.order_by('-number_of_likes')
            case 'commented':
                posts = posts.order_by('-number_of_comments')
            case _:
                posts = posts.order_by('-created_at')
        return posts
