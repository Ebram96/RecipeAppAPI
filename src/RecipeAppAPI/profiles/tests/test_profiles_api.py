from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from profiles.tests.helpers import create_user


CREATE_USER_URL = reverse("profiles:create")


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
