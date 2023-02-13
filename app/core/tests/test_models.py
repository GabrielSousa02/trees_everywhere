"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Profile


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)

    def test_new_user_email_normalized(self):
        """Test if email is normalized for new users"""
        sample_emails = [
            ('test1@EXAMPLE.com', 'test1@example.com'),
            ('Test2@Example.com', 'Test2@example.com'),
            ('TEST3@EXAMPLE.COM', 'TEST3@example.com'),
            ('test4@example.COM', 'test4@example.com'),
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that a new User without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_create_superuser(self):
        """Test superuser creation."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_profile(self):
        """Test user profile creation."""
        # Set test data
        email = 'test@example.com'
        password = 'sample123'
        about = 'This an about information, regarding an awesome user.'
        # Create test user
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            user_about=about,
        )
        # Execute assertions
        self.assertTrue(isinstance(user.profile, (Profile)))
        self.assertEqual(user.profile.user_about, about)
