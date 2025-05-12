from rest_framework.response import Response
from rest_framework import status

from ..interfaces.pydantic.user import IPY_SignUp

from ..repositories.user import UserRepository


class UserController:
    def __init__(self) -> None:
        self._userrepo = UserRepository()

    def signup_user(self, user_data: IPY_SignUp) -> Response:
        user = self._userrepo.create_user(user_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get_user(self, user_id) -> Response:
        user = self._userrepo.get_user(user_id)
        return Response(UserSerializer(user).data)
