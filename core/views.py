from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django.db.models import Q

from .models import Post
from .forms import AddPostForm, FilterForm


class HomeView(ListView):
    model = Post
    template_name = 'core/home.html'
    paginate_by = 6

    filtered_qs = None

    def get_context_data(self, *args):
        context = super().get_context_data()
        context['filter_form'] = FilterForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        return queryset.order_by('-title')


class AddPostView(CreateView):
    model = Post
    template_name = 'core/add-post.html'
    form_class = AddPostForm
    success_url = None

    def get_success_url(self):
        return reverse('home')

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()
        initial['name'] = ''
        initial['description'] = ''
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(self.get_success_url())

    def get(self, request, *args):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse('home'))
        return super().get(request)


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'


class PostDeleteView(DeleteView):
    model = Post
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get_success_url(self):
        return reverse('home')

    def get(self, *args, **kwargs):
        slug = kwargs.get('slug')
        post = Post.objects.get(slug=slug)

        if self.request.user != post.author:
            return HttpResponseRedirect(redirect_to=reverse('home'))

        return super().get(*args, **kwargs)
