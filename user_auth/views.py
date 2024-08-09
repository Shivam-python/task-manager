from rest_framework.versioning import NamespaceVersioning
from rest_framework.permissions import AllowAny
from task_management.views.base_api_view import BaseAPIView
from user_auth.helpers.function_helpers.registration import (
    register_user,
    verify_user
)
from user_auth.serializers import UserSerializer, UserVerificationSerializer


# Create your views here.

class VersioningConfig(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'


class UserSignup(BaseAPIView):
    versioning_class = VersioningConfig
    permission_classes = [AllowAny]
    serializer_classes = {
        "POST": UserSerializer
    }

    def handle_post_v1(self, request, *args, **kwargs):
        validated_data = request.validated_data
        return register_user(validated_data)


class UserVerification(BaseAPIView):
    versioning_class = VersioningConfig
    permission_classes = [AllowAny]
    serializer_classes = {
        "POST": UserVerificationSerializer
    }

    def handle_post_v1(self, request, *args, **kwargs):
        validated_data = request.validated_data
        return verify_user(validated_data)
