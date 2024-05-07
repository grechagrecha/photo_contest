from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from apps.users.mixins import TokenRequiredMixin
from core.forms import PostUpdateForm
from core.models import Post


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
