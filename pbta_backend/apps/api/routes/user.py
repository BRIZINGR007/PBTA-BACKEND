from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..controllers.user import UserController
from ..interfaces.pydantic.user import IPY_SignUp


@api_view(["GET"])
def get_user(request, user_id):
    user_data = UserController().get_user(user_id)
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_user(request):
    user_data = IPY_SignUp(**request.data)
    return UserController().signup_user(user_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    pass
