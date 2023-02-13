"""
Database models for Accounts.
"""
from django.db import models, IntegrityError

from core.models import User


class Account(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField('core.user')

    def add_member(self, user):
        """Adds specific User to the Account"""
        # Query the DB to find the User
        user_to_add = User.objects.get(email=user.email)
        # Check if query had no problem
        if not user_to_add:
            return False, IntegrityError
        # Add the User to the members field
        self.members.add(user_to_add.id)
        # Save the new state of the Account
        self.save()
        # Return the status and the added User
        return True, user_to_add
