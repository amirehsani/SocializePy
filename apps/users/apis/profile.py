from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from apps.api.mixins import APIAuthMixin

from drf_spectacular.utils import extend_schema

from apps.users.models import Profile
from apps.users.selectors.user import get_profile


class ProfileAPI(APIAuthMixin, APIView):
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ("bio", "posts_count", "subscriber_count", "subscription_count")

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            cache_profile = cache.get(f"profile_{instance.user}", {})
            if cache_profile:
                rep["posts_count"] = cache_profile.get("posts_count")
                rep["subscriber_count"] = cache_profile.get("subscribers_count")
                rep["subscription_count"] = cache_profile.get("subscriptions_count")

            return rep

    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutPutSerializer(query, context={"request": request}).data)
