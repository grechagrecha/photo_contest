from django.core.exceptions import ImproperlyConfigured


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
        request.META['HTTP_AUTHORIZATION'] = request.user.token
