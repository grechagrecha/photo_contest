from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from apps.users.mixins import TokenRequiredMixin
from core.models import Like


# TODO: Спросить у ментора и переделать LikeView
class PostLikeView(TokenRequiredMixin, View):
    def post(self, *args, **kwargs):
        slug = kwargs.get('slug')
        Like.like_toggle(self.request.user, slug)
        return HttpResponseRedirect(redirect_to=f'{reverse("home")}#{slug}')
