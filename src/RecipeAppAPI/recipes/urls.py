from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet


router = DefaultRouter()
router.register("tags", TagViewSet)

app_name = "recipes"
urlpatterns = [
    path("", include(router.urls)),
]
