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
