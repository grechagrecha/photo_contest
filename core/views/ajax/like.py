from django.http import Http404, JsonResponse
from django.views.generic import View
from service_objects.services import ServiceOutcome

from core.services.like.toggle import LikeToggleService


class PostLikeAjaxView(View):
    def post(self, request, *args, **kwargs):
        does_req_accept_json = request.accepts('application/json')
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest' and does_req_accept_json

        if is_ajax_request:
            outcome = ServiceOutcome(
                LikeToggleService, {
                    'user': request.user,
                    'slug': kwargs['slug']
                }
            )
            
            return JsonResponse({'status': 200})
        return JsonResponse({'status': 404})
