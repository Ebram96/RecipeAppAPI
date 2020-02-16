from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Initializes tests requirements."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="ebram96@gmail.com",
            password="testAdmin123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create(
            email="testmail@gmail.com",
            password="testAdmin123"
        )

    def test_users_listed(self):
        """Test that users are listed in user page."""
        url = reverse("admin:core_userprofile_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """Test that user change page works"""
        url = reverse("admin:core_userprofile_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse("admin:core_userprofile_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
