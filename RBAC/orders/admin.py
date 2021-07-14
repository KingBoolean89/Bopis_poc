from django.contrib import admin
from .models import *

class ItemAdmin(admin.ModelAdmin):
    fields = ['name', 'desc', 'price']

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['orderID', 'timestamp']
    fields = ['items', 'customer', 'orderID', 'timestamp','status', 'orderType', 'customerEmail', 'parkingSpot', 'deliveryMethod', 'vehicleDetails', 'licensePlate']
    list_display = ( 'customer', 'orderID', 'timestamp', 'status', 'orderType')

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
