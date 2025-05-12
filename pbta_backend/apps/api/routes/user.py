from rest_framework.decorators import api_view
from rest_framework.response import Response

from pbta_backend.apps.api.controllers.user import UserController


@api_view(["GET"])
def get_user(request, user_id):
    user_data = UserController().get_user(user_id)
    return Response(user_data)
