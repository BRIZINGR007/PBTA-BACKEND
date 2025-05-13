from rest_framework.response import Response
from rest_framework import status

from ..services.user import UserService

from ..serializers.user import UserSerializer

from ..repositories.user import UserRepository


class UserController:
    def __init__(self) -> None:
        self._userrepo = UserRepository()
        self._userservice = UserService()

    def signup_user(self, user_data) -> Response:
        user = self._userservice.signup_user(user_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get_user(self, user_id) -> Response:
        user = self._userrepo.get_user(user_id)
        return Response(UserSerializer(user).data)
