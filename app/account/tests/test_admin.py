"""
Test for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from account.models import Account


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
            user_about='User',
        )
        self.account = Account.objects.create(
            name='Account01',
        )

    def test_accounts_list(self):
        """Test that accounts are listed on page."""
        url = reverse('admin:account_account_changelist')
        result = self.client.get(url)

        self.assertContains(result, self.account.name)

    def test_edit_account_page(self):
        """Test the edit account page works."""
        url = reverse('admin:account_account_change', args=[self.account.id])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

    def test_create_account_page(self):
        """Test the create user page works."""
        url = reverse('admin:account_account_add')
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
