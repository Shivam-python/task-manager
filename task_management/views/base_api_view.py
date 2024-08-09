import logging
from typing import Union
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.serializers import Serializer
import task_management.utils.custom_exceptions as ce
from task_management.common import messages as glob_messages

from task_management.utils.response_utils import ResponseHandler

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    versioning_class = None
    serializer_classes = {
        'GET': None,
        'POST': None,
        'PUT': None,
        'PATCH': None,
        'DELETE': None
    }
    method_slugs = None

    def get_serializer_class(self, request) -> Union[Serializer, None]:
        return self.serializer_classes.get(request.method)

    def common_validation(self, request, *args, **kwargs):
        self.check_method_slug(kwargs.get('method_slug'))
        self.validate_request(request)

    def validate_request(self, request):
        SerializerClass = self.get_serializer_class(request)
        if Serializer:
            data = request.data if request.method in ['POST', 'PUT', 'PATCH'] else request.query_params
            serializer = SerializerClass(data=data)
            if not serializer.is_valid():
                raise ce.ValidationFailed({
                    'message': glob_messages.VALIDATION_FAILED,
                    'data': serializer.errors
                })
            request.validated_data = serializer.validated_data

    def check_method_slug(self, method_slug):
        if method_slug and method_slug not in self.method_slugs:
            raise ce.InvalidSlug

    def get_handler(self, request, method_prefix):
        version = request.version
        handler_name = f"{method_prefix}_{version.replace('.', '_')}"
        handler = getattr(self, handler_name, None)
        if not handler:
            raise ce.VersionNotSupported(f"Version {version} is not supported.")
        return handler

    def get(self, request, *args, **kwargs):
        try:
            self.common_validation(request, *args, **kwargs)
            handler = self.get_handler(request, "handle_get")
            return handler(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def post(self, request, *args, **kwargs):
        try:
            self.common_validation(request, *args, **kwargs)
            handler = self.get_handler(request, "handle_post")
            return handler(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def put(self, request, *args, **kwargs):
        try:
            self.common_validation(request, *args, **kwargs)
            handler = self.get_handler(request, "handle_put")
            return handler(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def patch(self, request, *args, **kwargs):
        try:
            self.common_validation(request, *args, **kwargs)
            handler = self.get_handler(request, "handle_patch")
            return handler(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def delete(self, request, *args, **kwargs):
        try:
            self.common_validation(request, *args, **kwargs)
            handler = self.get_handler(request, "handle_delete")
            return handler(request, *args, **kwargs)
        except Exception as e:
            return self.handle_exception(e)

    def handle_exception(self, e):
        class_name = self.__class__.__name__
        if isinstance(e, ce.ValidationFailed):
            logger.error(f'{class_name} - API VIEW : {e}')
            return ResponseHandler.failure(message=e.detail['message'], data=e.detail['data'],
                                           status_code=status.HTTP_400_BAD_REQUEST)
        elif isinstance(e, ce.VersionNotSupported):
            logger.error(f'{class_name} - API VIEW : {e}')
            return ResponseHandler.failure(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        elif isinstance(e, ce.InvalidSlug):
            logger.error(f'{class_name} - API VIEW : {e}')
            return ResponseHandler.failure(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        elif isinstance(e, NotFound):
            logger.error(f'{class_name} - API VIEW : {e}')
            return ResponseHandler.failure(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f'{class_name} - API VIEW : {e}')
            return ResponseHandler.exception(message=str(e))
