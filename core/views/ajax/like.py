from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View
from service_objects.services import ServiceOutcome

from core.services.like.toggle import LikeToggleService


class PostLikeAjaxView(View):
    def post(self, request, *args, **kwargs):
        does_req_accept_json = request.accepts('application/json')
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest' and does_req_accept_json

        if not request.user.is_authenticated:
            return JsonResponse(data={'message': 'You need to be logged in to perform this action!'}, status=401)

        if not is_ajax_request:
            return JsonResponse({'message': 'Not an AJAX request!'}, status=403)

        outcome = ServiceOutcome(
            LikeToggleService, {
                'user': request.user,
                'slug': kwargs['slug']
            }
        )

        data = {'message': 'Post was successfully liked!'} | outcome.result
        return JsonResponse(data=data, status=200, safe=True)
