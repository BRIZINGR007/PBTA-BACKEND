import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from ..utils.jwt import JwtUtils
from ..context import set_current_user
from types import SimpleNamespace


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Try Authorization header first
        auth_header = request.headers.get("Authorization")
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1].strip()

        # Fallback to cookie if no token in Authorization header
        if not token:
            token = request.COOKIES.get("jwt")

        if not token:
            return None  # No token provided anywhere

        try:
            secret_key = JwtUtils.get_secret_key()
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        set_current_user(payload)
        user = SimpleNamespace(**payload, is_authenticated=True)
        return (user, token)
