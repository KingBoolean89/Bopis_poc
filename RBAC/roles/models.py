from django.db import models
from resources.models import Resource

class Role(models.Model):
    name = models.CharField(unique=True, max_length=75)
    resources = models.ManyToManyField(Resource, related_name='roles', blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name