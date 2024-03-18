from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def error_handler(exc: Exception, context: dict) -> Response:
    handlers = {
        'JWTException': _jwt_validation_error
    }

    response = exception_handler(exc, context)
    exc_class = exc.__class__.__name__

    if exc_class in handlers:
        return handlers[exc_class](exc, context)

    return response


def _jwt_validation_error(exc: Exception, context: dict) -> Response:
    return Response({'detail': 'token is invalid or expired'}, status.HTTP_400_BAD_REQUEST)
