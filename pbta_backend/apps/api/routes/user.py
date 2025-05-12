from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from pbta_backend.apps.api.controllers.user import UserController
from pbta_backend.apps.api.serializers.user import UserSerializer


@api_view(["GET"])
def get_user(request, user_id):
    user_data = UserController().get_user(user_id)
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.validated_data
        created_user = UserController().add_user(user_data)
        return Response(created_user, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
