from django.views.generic import ListView, CreateView, DetailView, DeleteView, View
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect, render
from django.db.models import Q

from .models import Post, Like, Comment
from .forms import AddPostForm, FilterForm


class HomeView(ListView):
    model = Post
    template_name = 'core/home.html'
    paginate_by = 6

    def post(self, *args, **kwargs):
        pass

    def get_context_data(self, *args):
        context = super().get_context_data()
        context['filter_form'] = FilterForm()

        likes_qs = Like.objects.filter(user=self.request.user)
        context['user_likes'] = list(map(lambda like: like.post.slug, likes_qs))
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(state='published')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)

        return context


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


class PostLikeView(View):
    def post(self, *args, **kwargs):
        slug = kwargs.get('slug')

        Like.like_toggle(self.request.user, slug)

        return HttpResponseRedirect(redirect_to=f'{reverse("home")}#{slug}')
