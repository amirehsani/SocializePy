from typing import Sequence, Type, TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_auth_header(headers):
    value = headers.get('Authorization')

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


if TYPE_CHECKING:
    from rest_framework.permissions import _PermissionClass
    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class APIAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
            JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, )
