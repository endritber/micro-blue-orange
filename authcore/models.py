from django.db import models
from django.contrib.auth.models import AbstractUser
from authcore.managers import UserClientManager
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User Authentication'


class UserClient(User):
    objects = UserClientManager()

    class Meta:
        proxy = True
        verbose_name = 'User Client'
