from django.urls import path

from ..routes import user


user_urls = [
    path("get_user/<int:user_id>/", user.get_user),
    path("signup/", user.signup_user),
    path("login/", user.login_user),
]
