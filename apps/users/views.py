from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialLogin
from django.dispatch import receiver
from django.views.generic import ListView, DetailView

from apps.users.models import User
from core.models import Post, Like
from core.paginator import SmartPaginator


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class YourPostsView(ListView):
    model = Post
    template_name = 'users/your_posts.html'
    paginate_by = 6
    paginator_class = SmartPaginator

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_paginator(self, *args, **kwargs):
        return self.paginator_class(*args, request=self.request)

    def get_queryset(self):
        queryset = self.model.objects.filter(
            author=self.request.user
        ).order_by('-created_at')
        requested_state = self.request.GET.get('post_state', None)

        if requested_state in Post.ModerationStates:
            queryset = (
                queryset.filter(
                    state=requested_state
                ).order_by('-created_at'))
        else:
            queryset = queryset.filter(
                state=self.model.ModerationStates.PUBLISHED
            ).order_by('-created_at')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            likes_qs = Like.objects.filter(user=self.request.user)
            context['user_likes'] = list(map(lambda like: like.post.slug, likes_qs))

        return context


@receiver(user_signed_up)
def populate_profile_from_vk(sociallogin: SocialLogin, user, **kwargs):
    extra_data: dict = sociallogin.account.extra_data
    user.username = f'{extra_data.get('first_name')} {extra_data.get('last_name')}'
    user.save()
