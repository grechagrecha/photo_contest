from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView

from apps.users.mixins import TokenRequiredMixin
from core.models import Comment


class CommentDeleteView(TokenRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '-confirm-delete'
    success_url = None

    def get(self, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = Comment.objects.get(pk=comment_id)

        if self.request.user != comment.user:
            return HttpResponseRedirect(redirect_to=self.get_success_url())

        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')
