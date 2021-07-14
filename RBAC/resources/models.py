from django.db import models

# Create your models here.
class Resource(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name