from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('events', EventViewset)



urlpatterns = [
    
] + router.urls