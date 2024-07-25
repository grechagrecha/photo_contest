from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from apps.users.mixins import TokenRequiredMixin
from core.forms import PostUpdateForm
from core.models import Post
from core.services.post.update import PostUpdateService


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

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')

        service = PostUpdateService()
        try:
            service.execute(request.POST.dict() | {'user': request.user, 'slug': slug}, request.FILES.dict())
        except Exception as e:
            return HttpResponse(e)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        return redirect(self.get_success_url())
