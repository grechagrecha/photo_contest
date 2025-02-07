from typing import List

from django.db.models import Q
from django.http import Http404, JsonResponse
from django.views import View
from service_objects.services import ServiceOutcome

from apps.api.serializers import AjaxSearchJsonSerializer
from core.models import Like
from core.paginator import SmartPaginator
from core.services.ajax.search import AjaxSearchService
from core.settings import HOME_PAGE_SIZE


class PostSearchAjaxView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query')
        current_page = request.GET.get('page', 1)
        does_req_accept_json = request.accepts('application/json')
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest' and does_req_accept_json

        if is_ajax_request:
            posts_qs = ServiceOutcome(AjaxSearchService, {'search_query': search_query}).result
            paginator = SmartPaginator(posts_qs, HOME_PAGE_SIZE, request=self.request)

            print(current_page)
            print(request.GET)
            page_obj = paginator.get_page(current_page)
            

            serializer = AjaxSearchJsonSerializer(
                page_obj,
                many=True
            )
            return JsonResponse(data={'data': serializer.data, 'status': 200})
        return Http404
