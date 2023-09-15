from django.urls import path
from .apis.post import PostAPI, PostDetailAPI
from .apis.subscription import SubscribeApi, SubscribeDetailApi


urlpatterns = [
    path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
    path("subscribe/<str:email>", SubscribeDetailApi.as_view(), name="subscribe_detail"),
    path("post/", PostAPI.as_view(), name="post"),
    path("post/<slug:slug>", PostDetailAPI.as_view(), name="post_detail"),
]
