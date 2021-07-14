from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from .serializers import *
from .models import *
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination

class EventViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    pagination_class = CustomPagination
    permission_classes =[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','timestamp', 'action', 'user', 'role', 'resource']
    ordering_fields = ['id','timestamp', 'action', 'user', 'role', 'resource']
    search_fields = ['id','timestamp', 'action', 'user', 'role', 'resource']