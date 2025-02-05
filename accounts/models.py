from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    mobile = models.CharField(max_length=15, unique=True)  # Ensure mobile is unique
    username = models.CharField(max_length=150, unique=True)  # Enforce unique username

    def __str__(self):
        return self.email
    # Fixing the reverse accessor conflict
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change the related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change the related_name
        blank=True
    )
