from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView

from apps.users.mixins import TokenRequiredMixin
from core.forms import CommentUpdateForm
from core.models import Comment


class CommentUpdateView(TokenRequiredMixin, UpdateView):
    model = Comment
    template_name = 'core/comment-update.html'
    form_class = CommentUpdateForm
    success_url = None

    def get(self, *args, **kwargs):
        comment_slug = kwargs.get('slug')
        comment = self.model.objects.get(slug=comment_slug)

        if self.request.user != comment.user:
            messages.error(self.request, 'You are not the auhtor of the comment!')

            return HttpResponseRedirect(redirect_to=self.get_success_url())
        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')

    def get_initial(self):
        initial = super().get_initial()
        return initial
