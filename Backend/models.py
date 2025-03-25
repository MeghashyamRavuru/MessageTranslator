

from django.db import connection
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models, connection
from googletrans import Translator

translator = Translator()
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
        default='en'  # Default to English
    )

    def save(self, *args, **kwargs):
        # If the user is an admin and no language is set, default to English
        if self.is_superuser and not self.language:
            self.language = 'en'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    translated_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.message}"
    