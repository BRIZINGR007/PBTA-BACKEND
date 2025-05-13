from typing import cast
from ..repositories.user import UserRepository
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password


class UserService:
    def __init__(self) -> None:
        self._userrepo = UserRepository()

    def signup_user(self, user_data):
        user_data["password"] = make_password(user_data["password"])
        return self._userrepo.create_user(user_data)

    def login_user(self, user_data):
        try:
            user = self._userrepo.get_user_by_email(user_data["email"])
            if check_password(user_data["password"], cast(str, user.password)):
                return {"user": user}
            else:
                raise ValueError("Invalid password")
        except ObjectDoesNotExist:
            raise ValueError("User with this email does not exist")
