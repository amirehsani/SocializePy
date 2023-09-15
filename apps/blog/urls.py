from django.urls import path
from apps.blog.apis.products import ProductApi


urlpatterns = [
    path("product/", ProductApi.as_view(), name="product"),
]
