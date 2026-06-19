from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):

    ROLE_ADMIN = "ADMIN"
    ROLE_EMPLOYER = "EMPLOYER"
    ROLE_CANDIDATE = "CANDIDATE"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_EMPLOYER, "Employer"),
        (ROLE_CANDIDATE, "Candidate"),
    )

    username = None

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email