from rest_framework import serializers

from api.models import Link, ViewLog
from api.serializers import LinkSerializer
from api_user.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)
    links = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    def get_links(self, instance):
        links = Link.objects.filter(user=instance).all()
        return LinkSerializer(links, many=True).data

    def get_logs(self, instance):
        return ViewLog.objects.filter(user=instance).count()

    class Meta:
        model = User
        fields = '__all__'
        extra_fields = ['logs', 'links', ]
        extra_kwargs = {'password': {'write_only': True}}
