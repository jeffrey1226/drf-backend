from django.urls import re_path

from api_user.endpoint import auth

urlpatterns = [
    re_path(r'token', auth.AdminLoginView.as_view()),                   # Admin login
    re_path(r'user', auth.UserLoginView.as_view()),                     # User login
]
