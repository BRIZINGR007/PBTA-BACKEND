from django.urls import path
from ..controllers.user import UserController

urlpatterns = [
    path("", UserController().as_view(), name="users-list"),
    path("<int:user_id>/", UserController().as_view(), name="user-detail"),
]
