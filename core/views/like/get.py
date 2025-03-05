from django.http import JsonResponse
from django.views import View
from service_objects.services import ServiceOutcome

from core.services.like.get import LikeGetFromUserService


class LikeGetView(View):
    def get(self, request, *args, **kwargs):
        data = []
        post_slugs = request.GET.get('post_ids').split(', ')
        user_likes = ServiceOutcome(LikeGetFromUserService, {'user': request.user}).result
        print(f'User likes qs: {user_likes}')

        for like in user_likes.select_related('post'):
            if like.post.slug in post_slugs:
                data.append(like.post.slug)

        print(data)
        return JsonResponse(data=data, status=200, safe=False)
