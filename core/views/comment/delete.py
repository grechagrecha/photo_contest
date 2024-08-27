from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView
from service_objects.errors import ServiceObjectLogicError
from service_objects.services import ServiceOutcome

from apps.users.mixins import TokenRequiredMixin
from core.models import Comment
from core.services.comment.delete import CommentDeleteService
from core.services.comment.get import CommentGetService


class CommentDeleteView(TokenRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, request, *args, **kwargs):
        print(kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(CommentDeleteService, request.POST.dict() | kwargs | {'user': request.user})
            self.kwargs['post_slug'] = outcome.result
            return redirect(self.get_success_url())
        except ServiceObjectLogicError as e:
            messages.error(request, message=f'{e}')
            return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.kwargs['post_slug']})
