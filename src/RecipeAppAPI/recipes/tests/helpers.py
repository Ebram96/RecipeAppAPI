from django.contrib.auth import get_user_model

from core.models import Recipe


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
