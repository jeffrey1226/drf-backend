import random
import string

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_user.models import User, ResetPassword
from backend.settings import RESET_PASSWORD_LINK
from ctrl.email import send_reset_email


# User
class ForgotPasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email', None)

        if not email:
            return Response(
                data={
                    'title': 'Empty email',
                    'message': 'Empty email',
                    'error_code': 100
                },
                status=400
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                data={
                    'title': 'Empty user',
                    'message': 'Empty user',
                    'error_code': 101
                },
                status=400
            )

        code = ''.join(random.choice(string.digits) for x in range(6))
        ResetPassword.objects.create(
            user_id=user.id,
            email=email,
            code=code,
            is_active=True
        )

        username = user.profile_name
        if not username:
            username = user.username

        reset_link = RESET_PASSWORD_LINK.format(user.email, code)

        if send_reset_email(user.email, username, reset_link):
            return Response("success", status=200)
        else:
            return Response(
                data={
                    'title': 'Error',
                    'message': 'Error happened to send email',
                    'error_code': 102
                },
                status=400
            )


class ResetPasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email', None)
        code = self.request.data.get('code', None)
        password = self.request.data.get('password', None)

        if not email:
            return Response(
                data={
                    'title': 'Empty email',
                    'message': 'Empty email',
                    'error_code': 100
                },
                status=400
            )

        reset_password = ResetPassword.objects.filter(code=code, email=email).first()
        if not reset_password:
            return Response(
                data={
                    'title': 'Empty code',
                    'message': 'Email or code is invalid',
                    'error_code': 101
                },
                status=400
            )

        if not reset_password.is_active:
            return Response(
                data={
                    'title': 'Inactive code',
                    'message': 'Inactive code',
                    'error_code': 102
                },
                status=400
            )

        user = User.objects.filter(pk=reset_password.user_id).first()
        if not user:
            return Response(
                data={
                    'title': 'Empty user',
                    'message': 'Empty user',
                    'error_code': 103
                },
                status=400
            )

        user.set_password(password)
        user.save()

        reset_password.is_active = False
        reset_password.save()

        return Response("success", status=200)
