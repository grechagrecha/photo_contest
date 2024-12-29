from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

from core.services.post.recover import PostRecoverService


class PostRecoverView(View):
    slug_url_kwarg = 'post_slug'

    def post(self, request, *args, **kwargs):
        try:
            post_recovered = ServiceOutcome(
                PostRecoverService,
                request.POST.dict() | {
                    'user': request.user,
                    'post_slug': kwargs['post_slug']
                }
            ).result
        except Error as error:
            messages.error(request, f'Post was not recovered. Try again\n{error}')
            return redirect(reverse('home'))
        return redirect(self.get_success_url(post_recovered.slug))

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_slug': self.kwargs['post_slug']})
