from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class CustomManager(BaseUserManager):

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=25, blank=True)
    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return {self.email}

    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
