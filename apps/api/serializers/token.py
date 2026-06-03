from rest_framework import serializers
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.pk', read_only=True)

    class Meta:
        model = Token
        fields = ['key', 'user_id']
        