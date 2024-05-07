from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.mixins import TokenRequiredMixin
from core.forms import AddCommentForm
from core.models import Comment, Post


class CommentAddView(TokenRequiredMixin, CreateView):
    model = Comment
    template_name = 'core/comment-add.html'
    form_class = AddCommentForm
    success_url = None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse_lazy('post-detail', kwargs={'slug': slug})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        slug = self.kwargs.get('slug')
        comment.post = Post.objects.get(slug=slug)
        comment.save()
        return redirect(self.get_success_url())
