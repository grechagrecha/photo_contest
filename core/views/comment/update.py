from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView
from service_objects.services import ServiceOutcome

from core.forms import CommentUpdateForm
from core.models import Comment
from core.services.comment.update import CommentUpdateService


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'core/comment-update.html'
    form_class = CommentUpdateForm
    success_url = None
    slug_url_kwarg = 'comment_slug'

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CommentUpdateService,
            request.POST.dict() | {
                'comment_slug': kwargs['comment_slug'],
                'user': request.user
            }
        )

        updated_comment = outcome.result

        return redirect(self.get_success_url(updated_comment.post.slug))

    def get_success_url(self, post_slug):
        return reverse('post-detail', kwargs={'post_slug': post_slug})

    def get_initial(self):
        initial = super().get_initial()
        return initial
