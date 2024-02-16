from django.views.generic import ListView, CreateView, DetailView, DeleteView, View, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django.db.models import Q, Count, F

from apps.users.mixins import TokenRequiredMixin
from .models import Post, Like, Comment
from .forms import PostAddForm, FilterForm, AddCommentForm, PostUpdateForm
from .paginator import SmartPaginator


class HomeView(ListView):
    model = Post
    template_name = 'core/home.html'
    paginate_by = 6
    paginator_class = SmartPaginator

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_paginator(self, *args, **kwargs):
        return self.paginator_class(*args, request=self.request)

    def get_context_data(self, *args):
        context = super().get_context_data()
        context['filter_form'] = FilterForm()
        if self.request.user.is_authenticated:
            likes_qs = Like.objects.filter(user=self.request.user)
            context['user_likes'] = list(map(lambda like: like.post.slug, likes_qs))

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(state='published')
        search_query = self.request.GET.get('search_query', None)
        sorting_order = self.request.GET.get('ordering', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )

        if sorting_order == 'most_liked':
            return queryset.order_by('-number_of_likes')
        if sorting_order == 'most_commented':
            return queryset.order_by('-number_of_comments')
        if sorting_order == 'most_recent':
            return queryset.order_by('-created_at')
        return queryset.order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)

        return context


class PostAddView(TokenRequiredMixin, CreateView):
    model = Post
    template_name = 'core/post-add.html'
    form_class = PostAddForm
    success_url = None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        initial['name'] = ''
        initial['description'] = ''
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(self.get_success_url())


class PostUpdateView(TokenRequiredMixin, UpdateView):
    model = Post
    template_name = 'core/post-update.html'
    form_class = PostUpdateForm
    success_url = None

    def get(self, *args, **kwargs):
        slug = kwargs.get('slug')
        post = self.model.objects.get(slug=slug)

        if self.request.user != post.author:
            return HttpResponseRedirect(redirect_to=reverse('home'))

        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)

        # TODO: Change to only if image was changed
        post.state = self.model.ModerationStates.ON_VALIDATION
        post.save()
        return redirect(self.get_success_url())


class PostDeleteView(TokenRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, *args, **kwargs):
        slug = kwargs.get('slug')
        post = self.model.objects.get(slug=slug)

        if self.request.user != post.author:
            return HttpResponseRedirect(redirect_to=reverse('home'))

        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')


class PostLikeView(TokenRequiredMixin, View):
    def post(self, *args, **kwargs):
        slug = kwargs.get('slug')
        Like.like_toggle(self.request.user, slug)
        return HttpResponseRedirect(redirect_to=f'{reverse("home")}#{slug}')


class CommentAddView(TokenRequiredMixin, CreateView):
    model = Comment
    template_name = 'core/comment-add.html'
    form_class = AddCommentForm
    success_url = None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse('post-detail', kwargs={'slug': slug})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        slug = self.kwargs.get('slug')
        comment.post = Post.objects.get(slug=slug)
        comment.save()
        return redirect(self.get_success_url())


class CommentDeleteView(TokenRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = Comment.objects.get(pk=comment_id)

        if self.request.user != comment.user:
            return HttpResponseRedirect(redirect_to=self.get_success_url())

        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')
