from ..repositories.user import UserRepository
from ..serializers.user import UserSerializer
from django.contrib.auth.hashers import make_password


class UserService:
    def __init__(self) -> None:
        self._userrepo = UserRepository()

    def signup_user(self, user_data):
        user_data["password"] = make_password(user_data["password"])
        return self._userrepo.create_user(user_data)
