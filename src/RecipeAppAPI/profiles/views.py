from rest_framework import generics

from profiles.serializers import UserProfileSerializer


class CreateUserProfileView(generics.CreateAPIView):
    """Handles creating a new user object"""
    serializer_class = UserProfileSerializer
