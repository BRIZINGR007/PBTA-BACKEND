urlpatterns = [
    path("", UserController.as_view(), name="users"),
    path("<int:user_id>/", UserController.as_view(), name="user-detail"),
]
