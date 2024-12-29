from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from service_objects.errors import ServiceObjectLogicError
from service_objects.services import ServiceOutcome

from core.forms import CommentCreateForm
from core.models import Comment
from core.services.comment.get import CommentGetService
from core.services.comment.reply import CommentReplyService


class CommentReplyView(CreateView):
    model = Comment
    template_name = 'core/comment-create.html'
    form_class = CommentCreateForm
    success_url = None
    slug_url_kwarg = 'comment_slug'

    def post(self, request, *args, **kwargs):
        try:
            _ = ServiceOutcome(
                CommentReplyService,
                request.POST.dict() | {
                    'user': request.user,
                    'comment_slug': kwargs['comment_slug']
                }
            )
            return redirect(self.get_success_url())
        except ServiceObjectLogicError as e:
            messages.error(request, message=f'{e}')
            return redirect(reverse('comment-create'))

    def get_success_url(self):
        comment_slug = self.kwargs.get('comment_slug')
        post = ServiceOutcome(CommentGetService, {'comment_slug': comment_slug}).result.post
        return reverse_lazy('post-detail', kwargs={'post_slug': post.slug})

    def form_valid(self, form):
        return redirect(self.get_success_url())
