"""
Database models for Accounts.
"""
from django.db import models, IntegrityError

from core.models import User


class Account(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        'core.user',
        blank=True,
        related_name='accounts'
    )

    def __str__(self):
        return self.name

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

    def remove_member(self, user):
        """Adds specific User to the Account"""
        # Query the DB to find the User
        user_to_remove = User.objects.get(email=user.email)
        # Check if query had no problem
        if not user_to_remove:
            return False, IntegrityError
        # Find all planted trees by the user
        user_trees = user_to_remove.user_trees.all()
        # Find all planted trees part of the account
        account_trees = self.account_trees.all()
        # Remove the user trees from account trees
        for tree in set(user_trees).intersection(account_trees):
            account_trees.remove(tree)
        # Remove the User from the members field
        self.members.remove(user_to_remove.id)
        # Remove the Trees from the account trees field
        self.account_trees.set(account_trees)
        # Save the new state of the Account
        self.save()
        # Return the status and the removed User
        return True, user_to_remove
