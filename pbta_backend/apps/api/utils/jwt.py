import jwt
import datetime
from decouple import config
from rest_framework.response import Response


class JwtUtils:
    @staticmethod
    def create_jwt_token(user):
        """
        Creates a JWT token for the given user.

        Args:
            user: User object with user_id, email, and name attributes

        Returns:
            str: JWT token
        """
        payload = {
            "user_id": str(user.user_id),  # Convert UUID to string for JWT
            "email": user.email,
            "name": user.name,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=7),  # Token expires in 7 days
        }

        # Generate JWT token
        secret_key = config("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    @staticmethod
    def set_jwt_cookie(response, token, max_age=7 * 24 * 60 * 60):
        """
        Sets JWT cookie on the response.

        Args:
            response: Django response object
            token: JWT token string
            max_age: Cookie max age in seconds (default: 7 days)

        Returns:
            Response: Django response with cookie set
        """
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,  # Prevents JavaScript access
            secure=True,  # Only sent over HTTPS
            samesite="Strict",  # Restricts cross-site requests
            max_age=max_age,  # 7 days in seconds by default
        )

        return response

    @classmethod
    def create_jwt_response(
        cls, user, message="Login successful", status_code=200
    ) -> Response:
        """
        Creates a response with user data and sets JWT cookie.

        Args:
            user: User object
            message: Response message
            status_code: HTTP status code

        Returns:
            Response: Django response with user data and JWT cookie
        """
        # Create JWT token
        token = cls.create_jwt_token(user)

        # Create response with user data
        response = Response(
            {
                "message": message,
            },
            status=status_code,
        )

        # Set JWT cookie
        return cls.set_jwt_cookie(response, token)
