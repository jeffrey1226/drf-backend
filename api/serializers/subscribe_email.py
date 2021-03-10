from rest_framework import serializers

from api.models import SubscribeEmail


class SubscribeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeEmail
        fields = '__all__'
