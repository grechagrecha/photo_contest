from django.views.generic import ListView, CreateView
from .models import Post
from .filters import PostFilter


class HomeView(ListView):
    model = Post
    template_name = 'core/home.html'
    paginate_by = 6

    def get_context_data(self, *args):
        context = super().get_context_data()
        context['filter_form'] = PostFilter(self.request.GET, queryset=Post.objects.all())

        return context

    def get_queryset(self):
        return Post.objects.all().order_by('-name')


class AddPostView(CreateView):
    model = Post
    template_name = 'core/add-post.html'
    