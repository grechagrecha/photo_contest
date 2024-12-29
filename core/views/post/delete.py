from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DeleteView
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

from core.models import Post
from core.services.post.delete import PostDeleteService


class PostDeleteView(DeleteView):
    model = Post
    template_name_suffix = '-confirm-delete'
    success_url = None
    slug_url_kwarg = 'post_slug'

    def post(self, request, *args, **kwargs):
        try:
            _ = ServiceOutcome(
                PostDeleteService,
                request.POST.dict() | {
                    'user': request.user,
                    'post_slug': kwargs['post_slug']
                }
            )
        except Error as e:
            messages.error(request, f'Something unexpected happened: {e}')
            return redirect(reverse('post-detail', kwargs={'post_slug': kwargs.get('post_slug')}))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('users:profile')
