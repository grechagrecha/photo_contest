from typing import List
from django.http import Http404, JsonResponse
from django.views import View
from django.db.models import Q

from core.models import Post
from apps.api.serializers import AjaxSearchJsonSerializer


class PostSearchAjaxView(View):

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query')
        does_req_accept_json = request.accepts('application/json')
        is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest' and does_req_accept_json

        if is_ajax_request:
            posts = Post.objects.filter(
                Q(state=Post.ModerationStates.PUBLISHED) |
                Q(state=Post.ModerationStates.ON_DELETION)
            )

            if search_query:
                posts = posts.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(author__username__icontains=search_query))

            serializer = AjaxSearchJsonSerializer(posts, many=True)
            posts = list(posts.values().order_by('-created_at'))

            return JsonResponse(data={'data': serializer.data, 'status': 200})
        return Http404
