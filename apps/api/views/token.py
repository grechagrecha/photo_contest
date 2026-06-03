from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome

from ..serializers import TokenSerializer
from ..services import TokenGetOrCreateService


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token_obj = ServiceOutcome(
            TokenGetOrCreateService,
            {'user': user}
        ).result
        token_serializer = TokenSerializer(token_obj)
        return Response(data={
            'user_id': token_serializer.data['user_id'],
            'token': token_serializer.data['key']
        })
