from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from service_objects.errors import ServiceObjectLogicError
from service_objects.services import ServiceOutcome

from core.forms import CommentCreateForm
from core.models import Comment
from core.services.comment.create import CommentCreateService


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'core/comment-create.html'
    form_class = CommentCreateForm
    success_url = None

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CommentCreateService,
                request.POST.dict() | {
                    'slug': self.kwargs['slug'],
                    'user': request.user
                }
            )
            return redirect(self.get_success_url())
        except ServiceObjectLogicError as e:
            messages.error(request, message=f'{e}')
            return redirect(reverse('comment-create'))

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse_lazy('post-detail', kwargs={'slug': slug})

    def form_valid(self, form):
        return redirect(self.get_success_url())
