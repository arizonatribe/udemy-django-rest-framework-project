from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Helps Django work with a customized User model"""

    def create_user(self, email, name, password=None):
        """Creates a new user profile object"""

        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new super user"""

        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a user profile inside the API"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Helper (class) function to get the full name of the user."""

        return self.name

    def get_short_name(self):
        """Helper (class) function to get the user's short name."""

        return self.name

    def __str__(self):
        """Required implementation to convert the user model to a string."""

        return self.email
