from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    instagram_password = models.CharField(max_length=128)
    user_id = models.CharField(max_length=255, blank=True, null=True)
