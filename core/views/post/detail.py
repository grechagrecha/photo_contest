from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

from core.models import Post, Comment
from core.services.post.get import PostGetService


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'

    def get(self, request, *args, **kwargs):
        super().get(request, args, kwargs)
        context = self.get_context_data()
        try:
            outcome = ServiceOutcome(PostGetService, kwargs)
            context['result'] = outcome.result
        except Error as error:
            messages.error(request, message=f'{error}')
            return redirect(reverse('home'))
        return render(request, self.template_name, context, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)

        return context
