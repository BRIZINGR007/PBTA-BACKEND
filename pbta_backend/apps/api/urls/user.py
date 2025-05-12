from django.urls import path

from pbta_backend.apps.api.routes import user


urlpatterns = [
    path("get_user/<int:user_id>/", user.get_user),
    path("add-user/", user.add_user),
]
