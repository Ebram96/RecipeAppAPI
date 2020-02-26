from django.urls import path

from profiles.views import CreateUserProfileView


app_name = "profiles"
urlpatterns = [
    path("create/", CreateUserProfileView.as_view(), name="create")
]
