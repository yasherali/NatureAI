from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=20)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions_set',
        blank=True,
    )
