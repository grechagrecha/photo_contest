from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from service_objects.errors import Error
from service_objects.services import ServiceOutcome

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
        try:
            outcome = ServiceOutcome(
                PostCreateService,
                request.POST.dict() | {'user': request.user},
                request.FILES.dict()
            )
        except Error as error:
            # TODO: Change to more general implementation
            for e in error.errors_dict.get('title'):
                messages.add_message(request, messages.INFO, e)
            return redirect('post-create')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = ''
        initial['description'] = ''
        return initial

    def form_valid(self, form):
        return redirect(self.get_success_url())
