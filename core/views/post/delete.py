from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView

from apps.users.mixins import TokenRequiredMixin
from core.models import Post


class PostDeleteView(TokenRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, *args, **kwargs):
        slug = kwargs.get('slug')
        post = self.model.objects.get(slug=slug)

        if self.request.user != post.author:
            return HttpResponseRedirect(redirect_to=reverse('home'))

        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')
