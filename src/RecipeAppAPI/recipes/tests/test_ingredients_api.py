from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipes.tests.helpers import create_user
from recipes.serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipes:ingredient-list")


class PublicIngredientAPITests(TestCase):
    """Tests for Ingredient model for not logged in users"""
    def setUp(self):
        self.client = APIClient()

    def test_ingredient_list_login_required(self):
        """Test login is required when trying to retrieve ingredients list"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """Test ingredients API for logged in users"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="ebram96@gmail.com", password="TestPass")

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list_successful(self):
        """
        Test retrieving ingredients list for logged in users is successful
        """
        Ingredient.objects.create(user=self.user, name="Milk")
        Ingredient.objects.create(user=self.user, name="Sugar")

        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredients_limited_to_authorized_user(self):
        """Test returned tag list is limited to the authenticated user"""
        another_user = create_user(
            email="another96@gmail.com",
            password="testPassword",
        )
        Ingredient.objects.create(user=another_user, name="Milk")
        ingredient = Ingredient.objects.create(user=self.user, name="Sugar")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredient_with_valid_data_successful(self):
        """Test creating ingredient with valid data is successful"""
        payload = {"name": "Milk"}
        res = self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload["name"],
        ).exists()
        self.assertEqual(exists, True)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_ingredient_with_invalid_data_fail(self):
        """Test creating ingredient with invalid data is failing"""
        payload = {"name": ""}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
