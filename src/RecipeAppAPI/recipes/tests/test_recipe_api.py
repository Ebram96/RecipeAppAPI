from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipes.tests.helpers import create_user, sample_recipe
from recipes.serializers import RecipeSerializer

from core.models import Recipe


RECIPE_URL = reverse("recipes:recipe-list")


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated Recipe model API access"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated access to Recipe API model"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="ebram96@gmail.com", password="testPass")
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes_list_success(self):
        """Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_logged_user_success(self):
        """Test retrieving recipes for logged user only"""
        another_user = create_user(email="another@gmail.com", password="testP")
        sample_recipe(user=another_user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
