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
