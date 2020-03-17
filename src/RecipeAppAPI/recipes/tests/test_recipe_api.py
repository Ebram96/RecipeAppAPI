from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipes.tests.helpers import (
    create_user,
    sample_recipe,
    sample_tag,
    sample_ingredient,
    recipe_detail_url
)
from recipes.serializers import RecipeSerializer, RecipeDetailSerializer

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

    def test_retrieve_recipe_detail_success(self):
        """Test retrieving a Recipe detail is correct and successful"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        res = self.client.get(recipe_detail_url(recipe.id))
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe_success(self):
        """Test creating a Recipe is successful"""
        payload = {
            "title": "Koshary",
            "time_minutes": 40,
            "price": 10,
        }
        res = self.client.post(RECIPE_URL, payload)
        recipe = Recipe.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags_success(self):
        """Test creating a Recipe with some tags is successful"""
        tag1 = sample_tag(user=self.user, name="Local")
        tag2 = sample_tag(user=self.user, name="Fast")
        payload = {
            "title": "Koshary",
            "tags": [tag1.id, tag2.id],
            "time_minutes": 40,
            "price": 10,
        }
        res = self.client.post(RECIPE_URL, payload)
        recipe = Recipe.objects.get(id=res.data["id"])
        tags = recipe.tags.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients_successful(self):
        """Test creating a Recipe with some ingredients is successful"""
        ingredient1 = sample_ingredient(user=self.user, name="Milk")
        ingredient2 = sample_ingredient(user=self.user, name="Salt")
        payload = {
            "title": "Bashamel",
            "ingredients": [ingredient1.id, ingredient2.id],
            "time_minutes": 45,
            "price": 10,
        }
        res = self.client.post(RECIPE_URL, payload)
        recipe = Recipe.objects.get(id=res.data["id"])
        ingredients = recipe.ingredients.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
