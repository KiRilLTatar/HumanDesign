from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    timezone = models.CharField("Часовой пояс", max_length=50, default="UTC")

