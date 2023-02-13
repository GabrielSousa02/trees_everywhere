"""
Tests for Account models.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from account.models import Account


class ModelTests(TestCase):
    """Teste Account models."""

    def setUp(self):
        """Create user and client."""
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_create_account_successful(self):
        """Test creating an Account is successful."""
        name = 'Account 01'
        is_active = True
        account = Account.objects.create(
            name=name,
            is_active=is_active,
        )

        self.assertEqual(account.name, name)
        self.assertEqual(account.is_active, is_active)

    def test_create_inactive_account(self):
        """Test creating an inactive Account."""
        name = "Account 02"
        is_active = False
        account = Account.objects.create(
            name=name,
            is_active=is_active,
        )

        self.assertEqual(account.name, name)
        self.assertEqual(account.is_active, is_active)

    def test_add_users_to_account(self):
        """Test adding users to Account."""
        name = "Account 02"
        account = Account.objects.create(
            name=name
        )
        result = account.add_member(self.user)

        self.assertTrue(result[0], True)
        self.assertEqual(result[1].email, 'user@example.com')
