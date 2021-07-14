from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()

router.register('items', ItemViewset)
router.register('orders', OrderViewset)



urlpatterns = [
    path('api/commerce/shipments/<int:id>/tasks/AcceptShipment/completed', accept_shipment),
    path('api/commerce/shipments/<int:id>/tasks/PrintPickList/completed', print_pick_list),
    path('api/commerce/shipments/<int:id>/tasks/ValidateItemsInStock/completed', validate_stock),
    path('api/commerce/shipments/<int:id>/tasks/CustomerPickup/completed', customer_accepted),
    path('api/commerce/shipments/<int:id>/canceled', customer_en_route),
    path('api/commerce/shipments/<int:id>/customerAtCurbside', customer_curbside),
    path('api/<int:id>/pushNotification', register_push_notifications),
] + router.urls