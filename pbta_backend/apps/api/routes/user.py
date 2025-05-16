from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..serializers.user import SignupSerializer, LoginSerializer

from ..controllers.user import UserController


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_user(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_data = serializer.validated_data
    return UserController().signup_user(user_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    login_data = serializer.validated_data
    return UserController().login_user(login_data)


@api_view(["GET"])
def validate_session(request):
    return Response(
        {"message": "Succesfully Validated  Session."}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def logout(request):
    return UserController().logout_user()
