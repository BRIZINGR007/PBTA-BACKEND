from typing import cast
import jwt
import datetime
from decouple import config
from rest_framework.response import Response

SECRET_KEY = cast(str, config("SECRET_KEY"))


class JwtUtils:
    @staticmethod
    def get_secret_key() -> str:
        return SECRET_KEY

    @classmethod
    def create_jwt_token(cls, user):
        payload = {
            "user_id": str(user.user_id),
            "email": user.email,
            "name": user.name,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=7),
        }
        secret_key = cls.get_secret_key()
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    @staticmethod
    def set_jwt_cookie(response, token, max_age=7 * 24 * 60 * 60):
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=max_age,
        )
        return response

    @classmethod
    def create_jwt_response(
        cls, user, message="Login successful", status_code=200
    ) -> Response:
        token = cls.create_jwt_token(user)
        response = Response(
            {
                "message": message,
            },
            status=status_code,
        )
        return cls.set_jwt_cookie(response, token)
