from django.core.validators import MinLengthValidator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import BaseUser
from apps.users.services.user import create_user
from apps.utils.validators import number_validator, special_char_validator, letter_validator


token = serializers.SerializerMethodField("get_token")


class RegisterAPI(APIView):

    class InputRegisterSerializer(serializers.Serializer):

        email = serializers.CharField(max_length=255)
        password = serializers.CharField(validators=[
                                         number_validator,
                                         special_char_validator,
                                         letter_validator,
                                         MinLengthValidator(limit_value=8),
                                         ])
        confirm_password = serializers.CharField(max_length=31)

        @staticmethod
        def validate_email(email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exists!")

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please provide us with a password and confirmation")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Please confirm your password again.")

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("email", "token", "created_at", "updated_at")

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):

        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_user(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(self.OutPutRegisterSerializer(query, context={"request": request}).data)

    @staticmethod
    def get_token(user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
