from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .func_views import *


router = DefaultRouter()

router.register('resources', ResourceViewset)



urlpatterns = [
    path('api/resources/role/<int:id>/', get_all_resources_access),
    path('api/delete/resource/<int:id>/', can_delete_resource),
    path('api/resource/access/<int:userid>/<int:id>/', check_resource_permission),
] + router.urls