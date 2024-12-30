from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from core.models import Post


class PostSearchAjaxView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query')

        posts = Post.objects.filter(
            Q(state=Post.ModerationStates.PUBLISHED) |
            Q(state=Post.ModerationStates.ON_DELETION)
        ).values()

        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__username__icontains=search_query)
            ).values()

        return JsonResponse(data=list(posts.order_by('-created_at')), status=200, safe=False)
