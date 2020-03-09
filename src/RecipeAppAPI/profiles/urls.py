from django.urls import path

from profiles.views import CreateUserProfileView, GenerateAuthTokenView


app_name = "profiles"
urlpatterns = [
    path("create/", CreateUserProfileView.as_view(), name="create"),
    path(
        "generateToken/",
        GenerateAuthTokenView.as_view(),
        name="generate_token"
    ),
]
