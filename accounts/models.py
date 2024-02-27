from django.db import models


from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .UserManager import MyUserManager
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    # avatar = models.ImageField(null=True, default="avatar.svg")
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = MyUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self):
        return self.email 

