import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from apps.users.models import User
from core.models import Post, Like
from core.paginator import SmartPaginator


class LoginView(DjangoLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('home')

    def form_invalid(self, form):
        print('Login form is invalid')
        return super().form_invalid(form)

    def form_valid(self, form):
        """
            TODO: Create a separate backend and take all this shit there
        """

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token = self._generate_token(username, password)
            user.token = token
            user.save()

            self.request.META['HTTP_AUTHORIZATION'] = token
            return super().form_valid(form)

        messages.error(self.request, 'Login failure! Check if the credentials are valid.')
        return HttpResponseRedirect(reverse('users:login'))

    def _generate_token(self, username, password):
        s = username + password + settings.SECRET_KEY
        s = s.encode('utf-8')
        token = hashlib.sha256(s).hexdigest()
        return token


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

        if requested_state:
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
