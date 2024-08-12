from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from apps.users.mixins import TokenRequiredMixin
from core.forms import PostAddForm
from core.models import Post
from core.services.post.create import PostCreateService


class PostAddView(TokenRequiredMixin, CreateView):
    model = Post
    template_name = 'core/post-create.html'
    form_class = PostAddForm
    success_url = None

    def post(self, request, *args, **kwargs):
        service = PostCreateService()
        try:
            service.execute(request.POST.dict() | {'user': request.user}, request.FILES.dict())
        except Exception as e:
            return HttpResponse(e)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        initial['name'] = ''
        initial['description'] = ''
        return initial

    def form_valid(self, form):
        return redirect(self.get_success_url())
