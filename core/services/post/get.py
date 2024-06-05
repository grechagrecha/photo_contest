from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import Service

from core.models import Post


class GetPostService(Service):
    slug = forms.SlugField()

    def process(self):
        slug = self.cleaned_data['slug']

        try:
            post = Post.objects.get(slug=slug)
            return post
        except ObjectDoesNotExist as e:
            print(e)
