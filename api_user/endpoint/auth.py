from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from api_user.models import User
from api_user.serializers import LoginSerializer, UserSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class AdminLoginView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user_object = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
        if not user_object:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )

        user = authenticate(username=user_object.username, password=password)

        if user is None:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )
        if not user.is_active:
            return Response(
                data={
                    'title': 'Deactivated user',
                    'message': 'That user is deactivated',
                    'error_code': 101
                },
                status=400
            )
        if not user.is_staff:
            return Response(
                data={'title': 'Invalid admin user',
                      'message': 'That user is not admin user',
                      'error_code': 102
                      },
                status=400
            )

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )

        return Response(
            data={
                'success': True,
                'token': jwt_token
            },
            status=200
        )


class UserLoginView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user_object = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
        if not user_object:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )

        user = authenticate(username=user_object.username, password=password)

        if user is None:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )
        if not user.is_active:
            return Response(
                data={
                    'title': 'Deactivated user',
                    'message': 'That user is deactivated',
                    'error_code': 101
                },
                status=400
            )
        if user.is_staff:
            return Response(
                data={
                    'title': 'Invalid admin user',
                    'message': 'That user is admin user',
                    'error_code': 102
                },
                status=400
            )

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )
        return Response(
            data={
                'success': True,
                'token': jwt_token,
                'user': UserSerializer(user).data
            },
            status=200
        )
