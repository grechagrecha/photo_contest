from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.mixins import TokenRequiredMixin
from core.forms import AddCommentForm
from core.models import Comment, Post
from core.services.comment.add import CommentAddService
from core.services.post.get import PostGetService


class CommentAddView(TokenRequiredMixin, CreateView):
    model = Comment
    template_name = 'core/comment-add.html'
    form_class = AddCommentForm
    success_url = None

    def post(self, request, *args, **kwargs):
        service = CommentAddService()
        post = PostGetService.execute({'slug': self.kwargs.get('slug')})

        try:
            service.execute(request.POST.dict() | {'user': request.user, 'post': post})
            return redirect(self.get_success_url())
        except Exception as e:
            return HttpResponse(e)

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse_lazy('post-detail', kwargs={'slug': slug})

    def form_valid(self, form):
        return redirect(self.get_success_url())
