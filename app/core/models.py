"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user.
        Password can be null for test porpoises and this is the
        default in django, so we keep it.
        extra fields is useful anytime we want to add fields to user model"""
        if not email:
            raise ValueError('User must have an email address.')

        # Because our Manager is associated to a model , we need a way to access
        # the model that we're associated with, and this is the way to do this
        # with the Django model manager
        # self.model will be the same as defining a new User object
        # out of our User class because that is the manager that our User
        # is going to be assigned to it.

        # So essentially we are creating a new User model

        user = self.model(email=self.normalize_email(email), **extra_fields)

        # set_password will encrypt the password
        user.set_password(password)

        # We are supporting multiple databases, just in case
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign the user    manager    to    our    custom    user    class
    objects = UserManager()

    # Defines the fields that we want to use for authentication
    USERNAME_FIELD = 'email'
