"""
Database models.
"""
from typing import List
from datetime import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from tree.models import Tree, PlantedTree, Location


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password, user_about, **extra_fields):
        """Create, save, and return a new user."""
        if not email:
            raise ValueError('User must have an email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create the Profile of an user
        user_profile = Profile.objects.create(user=user, user_about=user_about)
        # Saving it to the DB
        user_profile.save(using=self._db)
        # Adding the created profile to the User
        user.profile = user_profile
        return user

    def create_superuser(self, email, password, profile=None):
        """Create and return a new superuser."""
        user = self.create_user(
            email,
            password,
            user_about="An awsome superuser!"
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Profile(models.Model):
    """Profile of the user."""
    user = models.OneToOneField(
        'user',
        primary_key=True,
        on_delete=models.CASCADE
    )
    user_about = models.TextField(null=True, default='Awesome user!')
    user_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def plant_tree(self, tree: List[tuple]):
        """Create a PlantedTree record."""
        # Extract the name of the Tree
        tree_name = tree[0][0]
        # Extract location data
        tree_latitude = tree[0][1][0]
        tree_longitude = tree[0][1][1]
        # Query the DB to locate the Tree
        try:
            tree = Tree.objects.get(name=tree_name)
        except ObjectDoesNotExist:
            return (False, ObjectDoesNotExist)
        # Create the PlantedTree object
        new_planted_tree = PlantedTree.objects.create(
            age=0,
            planted_at=datetime.utcnow(),
            user=self,
            tree=tree,
        )
        # Save the PlantedTree to the DB
        new_planted_tree.save()
        # Add all accounts to the PlantedTree object
        new_planted_tree.account.set(self.accounts.all())
        # Create the location object
        new_location = Location.objects.create(
            planted_tree=new_planted_tree,
            latitude=tree_latitude,
            longitude=tree_longitude,
        )
        new_location.save()
        # Assign the location to the PlantedTree
        new_planted_tree.location = new_location
        new_planted_tree.save()

        return True, new_planted_tree

    def plant_trees(self, trees: List[tuple]):
        """Create multiple PlantedTree records."""
        planted_tree_return_status = []
        for tree in trees:
            # Extract the name of the Tree
            tree_name = tree[0]
            # Extract location data
            tree_latitude = tree[1][0]
            tree_longitude = tree[1][1]
            # Query the DB to locate the Tree
            try:
                tree = Tree.objects.get(name=tree_name)
            except ObjectDoesNotExist:
                planted_tree_return_status.append((False, ObjectDoesNotExist))
                continue
            # Create the PlantedTree object
            new_planted_tree = PlantedTree.objects.create(
                age=0,
                planted_at=datetime.utcnow(),
                user=self,
                tree=tree,
            )
            # Save the PlantedTree to the DB
            new_planted_tree.save()
            # Add all accounts to the PlantedTree object
            new_planted_tree.account.set(self.accounts.all())
            # Create the location object
            new_location = Location.objects.create(
                planted_tree=new_planted_tree,
                latitude=tree_latitude,
                longitude=tree_longitude,
            )
            new_location.save()
            # Assign the location to the PlantedTree
            new_planted_tree.location = new_location
            new_planted_tree.save()
            # Add the new PlantedTree to the return list of Trees
            planted_tree_return_status.append((True, new_planted_tree))

        return planted_tree_return_status
