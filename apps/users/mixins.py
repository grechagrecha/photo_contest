from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest


class TokenRequiredMixin(AccessMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION']
        
        if token is None:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
