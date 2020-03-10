from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipes.serializers import TagSerializer


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """Returns only tags that the currently logged user created"""
        return self.queryset.filter(creator=self.request.user)

    def perform_create(self, serializer):
        """Set the currently logged user as creator of a tag"""
        serializer.save(creator=self.request.user)
