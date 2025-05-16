import jwt
import datetime
from decouple import config
from rest_framework.response import Response

SECRET_KEY = "63b0a8f92bc010485c392c41d386c28be27b28cdcc1d7a23fb8be6668506ebf7931031824eb913e864e2e0479591fb0cb5decf0f3ef06407038dd8b24c720ceec5249ca4a9c6b7c2431cb81b1aecba8abc904919f389277dead75d03cc14dfd1ce0be985460eacf439215e64e941c898940c10d7dccceeea3b4b25e0e57b87cf71b108d8b53cfe1d892228ca6a9caff52b16f57ca93d32b7037b2a78e471d1062abc7e4e2eef4a440afc64dc6a5b26ccbb3d261ebd0a9ea7ee8d90c767fba9a8303e927ff3f2556d220309d6de3352f3b5af8509be4941c92002596635c7b2a6b794725dac59b88ed285e4c7bf0a2ce2273c0ccba7c333c4d6c8aa347c9a6535"


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
