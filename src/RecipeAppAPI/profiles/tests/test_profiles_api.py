from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from profiles.tests.helpers import create_user


CREATE_USER_URL = reverse("profiles:create")
GENERATE_AUTH_TOKEN_URL = reverse("profiles:generate_token")


class PublicUserAPITests(TestCase):
    """Test users API without authentication"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with a valid payload"""
        payload = {
            "email": "ebram96@gmail.com",
            "password": "testPassword",
            "name": "Ebram Shehata",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_exists(self):
        """Test creating a user with already existing data fails"""
        payload = {"email": "ebram96@gmail.com", "password": "testPassword"}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        """Test creating a new user with a password less than 8 character"""
        payload = {"email": "ebram96@gmail.com", "password": "test"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_valid_user(self):
        """Test a token is created for user with correct credentials"""
        payload = {"email": "ebram96@gmail.com", "password": "testPassword123"}
        create_user(**payload)
        res = self.client.post(GENERATE_AUTH_TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test a token is not created when wrong credentials provided"""
        create_user(email="ebram96@gmail.com", password="testPassword")
        payload = {"email": "ebram96@gmail.com", "password": "test"}
        res = self.client.post(GENERATE_AUTH_TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test a token is not created when user is not found"""
        payload = {"email": "ebram96@gmail.com", "password": "testPassword"}
        res = self.client.post(GENERATE_AUTH_TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test a token is not created when request payload is missing some
        credentials.
        """
        payload = {"email": "ebram96@gmail.com", "password": ""}
        res = self.client.post(GENERATE_AUTH_TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
