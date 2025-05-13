from django.urls import include, path
from .user import user_urls
from .expense_tracker import expense_tracker_urls

urlpatterns = [
    path("users/", include(user_urls)),
    path("expense-tracker/", include(expense_tracker_urls)),
]
