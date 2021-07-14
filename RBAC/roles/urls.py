from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .func_views import *


router = DefaultRouter()

router.register('roles', RoleViewset)



urlpatterns = [
    #Roles endpoint
    path('api/get_resources/<int:id>/', get_roles_resource),
    path('api/roles/users/<int:id>/', get_users_by_role),
    path('api/by_name/<str:name>/', get_by_name),
    path('api/remove_all/<int:id>/', remove_all_resources),
    path('api/remove_resource/<int:roleID>/<int:id>/', remove_roles_resource),
    path('api/roles/resource/<int:id>/', get_all_role_by_resource),
    path('api/delete/role/<int:id>/', can_delete_role),
] + router.urls