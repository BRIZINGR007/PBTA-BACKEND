from django.urls import path

from pbta_backend.apps.api.routes.user import get_user

urlpatterns = [
    path("get_user/<int:user_id>/", get_user),
]
