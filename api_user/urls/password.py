from django.urls import re_path

from api_user.endpoint import password

urlpatterns = [
    re_path(r'forgot', password.ForgotPasswordView.as_view()),
    re_path(r'reset', password.ResetPasswordView.as_view()),
]
