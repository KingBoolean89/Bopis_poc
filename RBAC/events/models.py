from django.db import models
from django.contrib.auth import get_user_model
from roles.models import *
from resources.models import *

User = get_user_model()

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=75)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Role, blank=True, on_delete=models.CASCADE, null=True)
    resource = models.ForeignKey(Resource, blank=True, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.action
