from django.views.generic import DetailView

from core.models import Post, Comment


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)

        return context
