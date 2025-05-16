from django.urls import path

from ..routes import user


user_urls = [
    path("signup/", user.signup_user),
    path("login/", user.login_user),
    path("validate-session/", user.validate_session),
    path("logout/", user.logout),
]
