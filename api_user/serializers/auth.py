from rest_framework import serializers

from api_user.models import User


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'password')
