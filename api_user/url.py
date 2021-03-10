from django.urls import path, include

urlpatterns = [
    path('user', include('api_user.urls.user')),
    path('auth', include('api_user.urls.auth')),
    path('password', include('api_user.urls.password')),
]
