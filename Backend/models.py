

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=50, choices=[
        ('English', 'English'),
        ('Telugu', 'Telugu'),
        ('Hindi', 'Hindi'),
        ('Tamil', 'Tamil'),
        ('Kannada', 'Kannada'),
    ])

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.username




