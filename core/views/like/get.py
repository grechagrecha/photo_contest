from django.http import JsonResponse
from django.views import View
from django.db.models import QuerySet
from service_objects.services import ServiceOutcome

from core.services.like.get import LikeGetFromUserService


class LikeGetView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return JsonResponse(data={'message': 'Can\'t get like from anonymous user.'}, status=200)
        
        data = []
        post_slugs = request.GET.get('post_ids').split(', ')
        user_likes = ServiceOutcome(LikeGetFromUserService, {'user': request.user}).result

        if not user_likes:
            return JsonResponse(data={'message': 'User has no likes.'}, status=200)

        for like in user_likes.select_related('post'):
            if like.post.slug in post_slugs:
                data.append(like.post.slug)

        return JsonResponse(data=data, status=200, safe=False)
