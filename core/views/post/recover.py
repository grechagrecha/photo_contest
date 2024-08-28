from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

from core.services.post.recover import PostRecoverService


class PostRecoverView(View):
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                PostRecoverService,
                request.POST.dict() | kwargs | {'user': request.user}
            )
        except Error as error:
            messages.error(request, f'Post was not recovered. Try again\n{error}')
            return redirect(self.get_success_url())
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.kwargs['slug']})
