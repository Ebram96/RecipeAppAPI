from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipes.serializers import TagSerializer
from recipes.tests.helpers import create_user


TAG_LIST_URL = reverse("recipes:tag-list")
USER_PAYLOAD = {"email": "ebram96@gmail.com", "password": "testPassword"}


class PublicTagAPITest(TestCase):
    """Represents tests for Tag model public APIs"""
    def setUp(self):
        self.client = APIClient()

    def test_tag_list_login_required(self):
        """Test login is required when trying to retrieve tags list"""
        res = self.client.get(TAG_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITests(TestCase):
    """Represents tests for Tag model public APIs"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**USER_PAYLOAD)
        self.client.force_authenticate(self.user)

    def test_retrieve_tag_list_successful(self):
        """Test retrieving list of tags"""
        Tag.objects.create(creator=self.user, name="Spicy")
        Tag.objects.create(creator=self.user, name="Well-Done")

        res = self.client.get(TAG_LIST_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_tags_limited_to_authorized_user(self):
        """Test returned tag list is limited to the authenticated user"""
        another_user = create_user(
            email="another_ebram96@gmail.com",
            password="testPassword",
        )
        Tag.objects.create(creator=another_user, name="Salad")
        Tag.objects.create(creator=self.user, name="Fruity")
        Tag.objects.create(creator=self.user, name="Salad")

        res = self.client.get(TAG_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # The data returned ordered by -name :
        self.assertEqual(res.data[0]["name"], "Salad")
        self.assertEqual(res.data[1]["name"], "Fruity")

        for tag in res.data:
            self.assertEqual(tag["creator"], self.user.id)
