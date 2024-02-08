from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.urls import reverse


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if not self.get_response:
            return ImproperlyConfigured('Middleware has encountered an error!')

        self.process_request(request)

        response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.user.is_authenticated:
            request.META['HTTP_AUTHORIZATION'] = f'token {request.user.token}'


class RestrictAccessToAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if not self.get_response:
            return ImproperlyConfigured('Middleware has encountered an error!')

        self.process_request(request)

        response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    raise Http404
            else:
                raise Http404
