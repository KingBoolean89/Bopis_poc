import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Item(models.Model):
    name = models.CharField(max_length=75)
    desc = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.99)
    quantity = models.IntegerField(default=3)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders', blank=True)
    customer = models.ForeignKey(User, blank=True, on_delete=models.DO_NOTHING, null=True)
    orderID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Open')
    orderType = models.CharField(max_length=50, default='Bopis')
    customerEmail = models.CharField(max_length=50, default='aking@everestech.com')
    parkingSpot = models.CharField(max_length=50, default='3A')
    deliveryMethod = models.CharField(max_length=50, default='Place in trunk')
    vehicleDetails = models.CharField(max_length=50, default='Red Toyota Camry')
    licensePlate = models.CharField(max_length=50, default='ABC12345')
    pushToken = models.CharField(max_length=50, default='Expo12345')

    class Meta:
        ordering = ['status']

    def __str__(self):
            return str(self.orderID)
    
