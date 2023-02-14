"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
