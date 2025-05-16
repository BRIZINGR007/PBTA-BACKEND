from rest_framework.response import Response
from rest_framework import status

from ..utils.jwt import JwtUtils

from ..services.user import UserService

from ..serializers.user import SignupSerializer

from ..repositories.user import UserRepository


class UserController:
    def __init__(self) -> None:
        self._userrepo = UserRepository()
        self._userservice = UserService()

    def signup_user(self, user_data) -> Response:
        self._userservice.signup_user(user_data)
        return Response(
            {"message": "Successfully Signed Up."}, status=status.HTTP_201_CREATED
        )

    def login_user(self, login_data) -> Response:
        try:
            result = self._userservice.login_user(login_data)
            user = result["user"]
            return JwtUtils.create_jwt_response(user)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {"error": "An error occurred during login"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_user(self, user_id) -> Response:
        user = self._userrepo.get_user(user_id)
        return Response(SignupSerializer(user).data)

    def logout_user(self) -> Response:
        response = Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="jwt",
            value="",  # Empty value
            max_age=0,  # Expire immediately
            httponly=True,  # HTTP-only flag
            secure=True,  # Secure flag (HTTPS only)
            samesite="None",  # Allow cross-site requests
            path="/",  # Ensure cookie is deleted from the correct path
        )
        return response
