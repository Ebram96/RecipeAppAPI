from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def create_sample_user():
    """Creates and returns a new user object."""
    return get_user_model().objects.create_user(
        email="ebram96@gmail.com",
        password="testPassword",
        name="Ebram Shehata",
    )


class ModelTests(TestCase):

    # Test user model
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful."""
        email = "ebram96@gmail.com"
        password = "modelTest123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email normalization for new users."""
        email = "ebram96@GMAIL.com"
        password = "testModel123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(email.lower(), user.email)

    def test_new_user_invalid_email(self):
        """Tests creating new user with no email raises an error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testModel123")

    def test_creating_new_superuser(self):
        """Tests creating a new user with superuser privileges."""
        email = "ebram96@gmail.com"
        password = "modelTest123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # Test Tag model
    def test_tag_str_representation_correct(self):
        """Test tag model object string representation is correct"""
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name="Spicy",
        )
        self.assertEqual(str(tag), tag.name)

    # Test Ingredient model
    def test_ingredient_str_representation_correct(self):
        """Test Ingredient model object string representation is correct"""
        ingredient = models.Ingredient.objects.create(
            user=create_sample_user(),
            name="Tomato"
        )
        return self.assertEqual(str(ingredient), ingredient.name)
