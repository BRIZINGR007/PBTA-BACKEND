from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.user import UserService
from ..serializers.user import UserSerializer


class UserController(APIView):
    def __init__(self) -> None:
        self._userservice = UserService()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self._userservice.create_user(serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get(self, user_id=None):
        if user_id:
            user = UserService.get_user(user_id)
            return Response(UserSerializer(user).data)
        all_users = self._userservice.get_all_users()
        return all_users
