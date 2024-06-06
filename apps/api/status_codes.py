from rest_framework import status
from rest_framework.exceptions import APIException


class ValidationError400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'


class ValidationError401(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'You need to be authorized to perform this action.'


class ValidationError403(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You are not authorized to perform this action.'


class ValidationError404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found. Sowwy.'
