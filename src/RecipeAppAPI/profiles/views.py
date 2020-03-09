from rest_framework import generics, permissions, authentication
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


class ManageUserProfileView(generics.RetrieveUpdateAPIView):
    """Manage a user data"""
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        """Get the current logged on user"""
        return self.request.user
