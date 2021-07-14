from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from roles.models import Role

class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users', blank=True)

    class Meta:
        ordering = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

