import jwt
from decouple import config
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from pbta_backend.apps.api.context import set_current_user


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        set_current_user(payload)
        return (payload, token)
