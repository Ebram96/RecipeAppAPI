from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from profiles.serializers import UserProfileSerializer, AuthTokenSerializer


class CreateUserProfileView(generics.CreateAPIView):
    """Handles creating a new user object"""
    serializer_class = UserProfileSerializer


class GenerateAuthTokenView(ObtainAuthToken):
    """Generates a new token for authenticated user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
