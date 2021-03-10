from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SubscribeEmail


class SubscribeEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = self.request.data["email"]
        subscribed = SubscribeEmail.objects.filter(email=email).first()
        if not subscribed:
            SubscribeEmail.objects.create(email=email, is_active=True)

        return Response(status=200)
