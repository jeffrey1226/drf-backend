from django.urls import re_path

from api.endpoint import subscribe_email

urlpatterns = [
    re_path(r'subscribe', subscribe_email.SubscribeEmailView.as_view()),
]
