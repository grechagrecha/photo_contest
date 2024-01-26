from django.views.generic import ListView, CreateView, DetailView, DeleteView, View
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django.db.models import Q

from .models import Post, Like, Comment
from .forms import AddPostForm, FilterForm, AddCommentForm
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

        if sorting_order == 'asc':
            return queryset.order_by('title')
        if sorting_order == 'desc':
            return queryset.order_by('-title')
        return queryset.order_by('-created_at')


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
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse('home'))

        slug = kwargs.get('slug')
        Like.like_toggle(self.request.user, slug)
        return HttpResponseRedirect(redirect_to=f'{reverse("home")}#{slug}')


class AddCommentView(CreateView):
    model = Comment
    template_name = 'core/add-comment.html'
    form_class = AddCommentForm
    success_url = None

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

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=self.get_success_url())
        return super().get(request)


class DeleteCommentView(DeleteView):
    model = Comment
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get_success_url(self):
        return reverse('home')

    def get(self, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = Comment.objects.get(pk=comment_id)

        if self.request.user != comment.user:
            return HttpResponseRedirect(redirect_to=self.get_success_url())

        return super().get(*args, **kwargs)
