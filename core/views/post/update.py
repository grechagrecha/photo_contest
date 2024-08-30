from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import UpdateView
from service_objects.errors import ServiceObjectLogicError
from service_objects.services import ServiceOutcome

from apps.users.mixins import TokenRequiredMixin
from core.forms import PostUpdateForm
from core.models import Post
from core.services.post.get import PostGetService
from core.services.post.update import PostUpdateService


class PostUpdateView(TokenRequiredMixin, UpdateView):
    model = Post
    template_name = 'core/post-update.html'
    form_class = PostUpdateForm
    success_url = None

    def get(self, *args, **kwargs):
        outcome = ServiceOutcome(PostGetService, kwargs)
        post = outcome.result

        if self.request.user != post.author:
            return HttpResponseRedirect(redirect_to=reverse('home'))

        return super().get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        slug = kwargs.get('slug')
        context = self.get_context_data()
        try:
            outcome = ServiceOutcome(
                PostUpdateService,
                request.POST.dict() | {'user': request.user, 'slug': slug},
                request.FILES.dict()
            )
        except ServiceObjectLogicError as error:
            return render(request, self.template_name, context | {'error_message': error}, status=500)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        return redirect(self.get_success_url())
