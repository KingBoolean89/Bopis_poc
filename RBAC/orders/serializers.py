from rest_framework import serializers
from .models import *
from users.serializers import UserSerializer

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    # customer = UserSerializer()
    items = ItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','items', 'orderID', 'status', 'timestamp', 'orderType', 'customerEmail', 'parkingSpot', 'deliveryMethod', 'vehicleDetails', 'licensePlate']