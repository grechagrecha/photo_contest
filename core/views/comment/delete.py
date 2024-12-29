from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DeleteView
from service_objects.errors import ServiceObjectLogicError
from service_objects.services import ServiceOutcome

from core.models import Comment
from core.services.comment.delete import CommentDeleteService


class CommentDeleteView(DeleteView):
    model = Comment
    template_name_suffix = '-confirm-delete'
    success_url = None
    slug_url_kwarg = 'comment_slug'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CommentDeleteService,
                request.POST.dict() | {
                    'user': request.user,
                    'comment_slug': kwargs['comment_slug']
                })
            
            post_slug = outcome.result.slug
            return redirect(self.get_success_url(post_slug))
        except ServiceObjectLogicError as e:
            messages.error(request, message=f'{e.errors_dict}')
            return redirect(reverse('home'))

    def get_success_url(self, post_slug):
        return reverse('post-detail', kwargs={'post_slug': post_slug})
