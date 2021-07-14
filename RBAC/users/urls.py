from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .func_views import *


router = DefaultRouter()

router.register('user', UserViewset)

urlpatterns = [
    path('remove_all_roles/<int:userid>/', remove_all_roles),
    path('user_resources/<int:userid>/', get_user_resources),
    path('remove_role/<int:userid>/<int:id>/', remove_users_role),
    path('user_roles/<int:userid>/', get_user_roles),
    path('access_roles/<int:userid>/', has_role_access),
    path('access_resources/<int:userid>/', has_resource_access),
    path('users/role/<int:id>/', get_all_user_access),
    path('users/resource/<int:id>/', get_all_user_by_resource),
] + router.urls