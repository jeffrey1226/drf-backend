from rest_framework import serializers

from api.models import ViewLog


class ViewLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewLog
        fields = '__all__'
