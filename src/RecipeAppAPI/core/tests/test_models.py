from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

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
