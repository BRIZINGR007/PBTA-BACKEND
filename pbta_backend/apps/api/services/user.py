from pbta_backend.apps.api.repositories.user import UserRepository


class UserService:
    def __init__(self) -> None:
        self._userrepo = UserRepository()
    
    def handle_user_signup(self , data):

