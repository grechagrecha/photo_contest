from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest

from apps.users.models import User


class TokenRequiredMixin(AccessMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token is None:
            return self.handle_no_permission()

        token = token.lstrip('token ')
        user: User = User.objects.get(token=token)

        if user is not None:
            # TODO: Add implementation
            pass

        return super().dispatch(request, *args, **kwargs)
