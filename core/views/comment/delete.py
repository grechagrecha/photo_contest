from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView

from apps.users.mixins import TokenRequiredMixin
from core.models import Comment
from core.services.comment.delete import CommentDeleteService
from core.services.comment.get import CommentGetService


class CommentDeleteView(TokenRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, *args, **kwargs):
        comment = CommentGetService.execute({'slug': self.kwargs.get('slug')})

        if self.request.user != comment.user:
            messages.error(self.request, 'You are not the author of the comment!')

            return HttpResponseRedirect(redirect_to=reverse('home'))

        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        service = CommentDeleteService()
        try:
            post_slug = service.execute({'slug': self.kwargs.get('slug')})
            return redirect(self.get_success_url(post_slug))
        except Exception as e:
            return HttpResponse(e)

    def get_success_url(self, post_slug):
        return reverse_lazy('post-detail', kwargs={'slug': post_slug})
