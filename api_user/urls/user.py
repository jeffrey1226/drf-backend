from django.urls import re_path

from api_user.endpoint import user

urlpatterns = [
    re_path(r'me', user.MeView.as_view()),                              # Get me
    re_path(r'profile', user.UserView.as_view()),                       # Get profile
    re_path(r'register', user.UserRegisterView.as_view()),              # User register
    re_path(r'update', user.UserUpdateView.as_view()),                  # User update
]
