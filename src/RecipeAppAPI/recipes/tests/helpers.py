from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Recipe, Tag, Ingredient


def create_user(**params):
    """
    Creates and returns a new user object from default authentication model
    """
    return get_user_model().objects.create_user(**params)


def sample_recipe(user, **params):
    """Creates and returns a sample recipe"""
    defaults = {
        "title": "Sample Recipe",
        "time_minutes": 10,
        "price": 20.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def recipe_detail_url(recipe_id):
    """Returns recipe detail URL"""
    return reverse("recipes:recipe-detail", args=(recipe_id,))


def recipe_image_upload_url(recipe_id):
    """Returns URL for recipe image upload"""
    return reverse("recipes:recipe-image-upload", args=(recipe_id,))


def sample_tag(user, name="Salad"):
    """Create and return a Tag object"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Milk"):
    """Create and return an Ingredient object"""
    return Ingredient.objects.create(user=user, name=name)
