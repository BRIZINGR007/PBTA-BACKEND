from ..models.user import User


class UserService:
    @staticmethod
    def create_user(data):
        return User.objects.create(**data)

    @staticmethod
    def get_user(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def get_all_users():
        return User.objects.all()
