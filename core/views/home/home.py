from django.db.models import Q
from django.views.generic import ListView

from core.forms import FilterForm
from core.models import Post, Like
from core.paginator import SmartPaginator


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
