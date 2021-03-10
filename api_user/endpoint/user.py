import base64
import uuid

from django.contrib.auth.models import update_last_login
from django.core.files.base import ContentFile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from api.models import ViewLog, Link
from api_user.models import User
from api_user.serializers import UserSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class MeView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get_object(self):
        user = User.objects.filter(pk=self.request.user.id).first()
        return user


class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        username = self.request.GET.get('username')

        user = User.objects.filter(username=username).first()
        if not user:
            return Response(
                data={
                    'title': 'No User',
                    'message': 'There is not user that has same username',
                    'error_code': 100
                },
                status=400
            )

        if not self.request.user or self.request.user.id != user.id:
            ViewLog.objects.create(
                user=user,
            )

        return Response(
            data=UserSerializer(user, context={"request": request}).data,
            status=200
        )


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = self.request.data['username']
        email = self.request.data['email']
        password = self.request.data['password']

        if User.objects.filter(username=username).first():
            return Response(
                data={
                    'title': 'Already Exist',
                    'message': 'There is already user that has same username',
                    'error_code': 100
                },
                status=400
            )

        if User.objects.filter(email=email).first():
            return Response(
                data={
                    'title': 'Already Exist',
                    'message': 'There is already user that has same email',
                    'error_code': 101
                },
                status=400
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response(
                data={
                    'title': 'Login error',
                    'message': 'Something went wrong. Please try again later',
                    'error_code': 102
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


class UserUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            return Response(
                data={
                    'title': 'Not found',
                    'message': 'User with given username and password does not exists',
                    'error_code': 100
                },
                status=400
            )

        for key in self.request.data:
            if key == 'profile_name':
                user.profile_name = self.request.data['profile_name']
            elif key == 'bio':
                user.bio = self.request.data['bio']
            elif key == 'password':
                user.set_password(self.request.data['password'])
            elif key == 'image':
                image = self.request.data['image']
                format, imgStr = image.split(';base64,')
                contentType = format.split(':')[-1]
                ext = format.split('/')[-1]
                if not contentType in ['image/png', 'image/jpeg']:
                    return Response(
                        data={
                            'title': 'Invalid file',
                            'message': 'Please select correct image file',
                            'error_code': 101
                        },
                        status=400
                    )

                avatar = ContentFile(base64.b64decode(imgStr), name=str(uuid.uuid4()) + '.' + ext)

                if user.avatar:
                    user.avatar.delete(False)

                user.avatar = avatar

            else:
                type = key
                social_link = self.request.data[key]
                link = Link.objects.filter(user=user, type=type).first()
                if link is None:
                    Link.objects.create(user=user, type=type, link=social_link)
                else:
                    link.link = social_link
                    link.save()

        user.save()

        return Response(status=200)
