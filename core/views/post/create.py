from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

from core.forms import PostCreateForm
from core.models import Post
from core.services.post.create import PostCreateService


class PostCreateView(CreateView):
    model = Post
    template_name = 'core/post-create.html'
    form_class = PostCreateForm
    success_url = None
    slug_url_kwarg = 'post_slug'

    def post(self, request, *args, **kwargs):
        try:
            post_created = ServiceOutcome(
                PostCreateService,
                request.POST.dict() | {'user': request.user},
                request.FILES.dict()
            ).result
        except Error as error:
            # TODO: Change to more general implementation
            for e in error.errors_dict.get('title'):
                messages.add_message(request, messages.INFO, e)
            return redirect('post-create')
        return redirect(self.get_success_url(post_created.slug))

    def get_success_url(self, post_slug):
        return reverse_lazy('post-detail', kwargs={'post_slug': post_slug})

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = ''
        initial['description'] = ''
        return initial

    def form_valid(self, form):
        return redirect(self.get_success_url())
