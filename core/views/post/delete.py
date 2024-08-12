from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from apps.users.mixins import TokenRequiredMixin
from core.models import Post
from core.services.post.delete import PostDeleteService


class PostDeleteView(TokenRequiredMixin, View):
    model = Post
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, *args, **kwargs):
        slug = kwargs.get('slug')

        try:
            service = PostDeleteService()
            service.execute({'slug': slug, 'user': self.request.user})
        except Exception as e:
            return HttpResponse(e)
        return redirect('home')

    def get_success_url(self):
        return reverse('home')
