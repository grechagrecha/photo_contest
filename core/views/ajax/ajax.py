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
        does_req_accept_json = request.accepts('application/json')
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest' and does_req_accept_json

        if is_ajax_request:
            posts_qs = ServiceOutcome(
                AjaxSearchService,
                {
                    'search_query': request.GET.get('search_query'),
                    'sort_order': request.GET.get('sort_order', 'recent')
                }
            ).result

            # user_likes = {}
            # if request.user.is_authenticated:
            #     print(request.user.like_set)
            #     user_likes = Like.objects.filter(user=request.user)
            # print(user_likes)

            page = self.get_posts_on_current_page(posts_qs)

            serializer = AjaxSearchJsonSerializer(
                page,
                many=True
            )
            return JsonResponse(data={'data': serializer.data, 'status': 200}, status=200)
        return Http404

    def get_posts_on_current_page(self, queryset):
        current_page = self.request.GET.get('page', 1)

        paginator = SmartPaginator(queryset, HOME_PAGE_SIZE, request=self.request)
        page_obj = paginator.get_page(current_page)
        return page_obj
