

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
    language = models.CharField(max_length=50, choices=[
        ('en', 'English'),
        ('te', 'Telugu'),
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
        ('kn', 'Kannada'),
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

def create_user_table(username):
    """Create a table for a user dynamically"""
    table_name = username.replace(" ", "_").lower()
    with connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                translated_message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    return table_name