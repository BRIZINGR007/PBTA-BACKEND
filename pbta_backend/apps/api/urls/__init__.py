from django.urls import include, path
from .user import user_urls

urlpatterns = [
    path("users/", include(user_urls)),
]
