

from django.db import connection
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models, connection
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    language = models.CharField(
        max_length=50,
        choices=[
            ('en', 'English'),
            ('te', 'Telugu'),
            ('hi', 'Hindi'),
            ('ta', 'Tamil'),
            ('kn', 'Kannada'),
        ],
        default='en'
    )

    def __str__(self):
        return self.username

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    translated_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted_by = models.JSONField(default=list)  # Stores deleted users (e.g., ["testuser1", "testuser2"])

    def is_fully_deleted(self):
        return len(self.deleted_by) == 2  # If both sender & receiver deleted, delete permanently
