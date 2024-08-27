from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DeleteView
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

from apps.users.mixins import TokenRequiredMixin
from core.models import Post
from core.services.post.delete import PostDeleteService


class PostDeleteView(TokenRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '-confirm-delete'
    success_url = None

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(PostDeleteService, request.POST.dict() | kwargs | {'user': request.user})
        except Error as e:
            messages.error(request, f'Something unexpected happened: {e}')
            return redirect(reverse('post-detail', kwargs={'slug': kwargs.get('slug')}))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('users:profile')
