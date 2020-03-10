from django.contrib.auth import get_user_model


def create_user(**params):
    """
    Creates and returns a new user object from default authentication model
    """
    return get_user_model().objects.create_user(**params)
