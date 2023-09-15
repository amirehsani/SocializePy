from django.urls import path
from apps.users.apis.profile import ProfileAPI
from apps.users.apis.register import RegisterAPI


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('profile/', ProfileAPI.as_view(), name='profile'),
]
