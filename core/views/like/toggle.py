from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from service_objects.services import ServiceOutcome

from apps.users.mixins import TokenRequiredMixin
from core.services.like.toggle import LikeToggleService


# TODO: Спросить у ментора и переделать LikeView
class LikeToggleView(TokenRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(LikeToggleService, {'user': request.user, 'slug': kwargs['slug']})
        return redirect(to=f'{reverse("home")}#{kwargs["slug"]}')
