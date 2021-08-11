from rest_framework import authentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.views import exception_handler
from rest_framework.response import Response


class StaticTokenAuthentication(authentication.BaseAuthentication):
    def get_token(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate(self, request):
        auth = self.get_token(request).split()
        
        if not auth or auth[0].lower() != b"token":
            raise exceptions.NotAuthenticated(
                "Authentication credentials were not provided.")

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.')

        if token != "abcdefghijklmnopqrstuvwxyz":
            raise exceptions.AuthenticationFailed('Invalid token.')
        return None


def handler(exc, context):
    if isinstance(exc, exceptions.NotAuthenticated):
        return Response({"details": "Authentication credentials were not provided."}, status=401)
    return exception_handler(exc, context)
