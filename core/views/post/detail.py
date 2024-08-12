from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from service_objects.services import ServiceOutcome

from core.models import Post, Comment
from core.services.post.get import PostGetService


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post-detail.html'

    def get(self, request, *args, **kwargs):
        super().get(request, args, kwargs)
        try:
            outcome = ServiceOutcome(PostGetService, kwargs)
        except Exception as error:
            return render(request, self.template_name, self.get_context_data() | {'error_message': error}, status=500)
        return HttpResponse(outcome.result, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)

        return context
