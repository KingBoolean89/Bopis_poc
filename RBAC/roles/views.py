from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
import sys
from django.db import IntegrityError
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.http import HttpResponse, HttpRequest, JsonResponse
from .serializers import *
from .models import *
from events.models import *
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination


class RoleViewset(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer 
    pagination_class = CustomPagination
    permission_classes =[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','name', 'resources']
    ordering_fields = ['id','name', 'resources']
    search_fields = ['id','name', 'resources']

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        try:
            if data == False:
                return HttpResponse(status=400)
            else:
                new_role = Role.objects.create(
                    name=data['name']
                )
                new_role.save()
                for resource in data['resources']:
                    resource_obj = Resource.objects.get(id=resource)
                    new_role.resources.add(resource_obj)
                serializer = RoleSerializer(new_role,data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                event = Event( 
                    timestamp=now(),
                    action='Role Created',
                    role=Role.objects.get(name=data['name'])
                )
                event.save()
                return Response(serializer.data)
        except IntegrityError: 
            return HttpResponse(status=400)

    def partial_update(self, request, pk, *args, **kwargs):
        data = request.data
        try:
            resources = data['resources']
            found_role = Role.objects.get(pk=pk)
            for resource in resources:
                print(resource)
                resource_obj = Resource.objects.get(id=resource)
                found_role.resources.add(resource_obj)
            serializer = RoleSerializer(found_role, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            event = Event( 
                    timestamp=now(),
                    action='Role Updated',
                    role=Role.objects.get(name=found_role.name)
                )
            event.save()
            print(event)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Role Does Not Exist'}) 
        except IntegrityError: 
            return JsonResponse({"error": 'That Name Already Exist'})
    
    def destroy(self, request, pk, *args, **kwargs):
        try:
            instance = self.get_object()
            event = Event( 
                    timestamp=now(),
                    action='Role Deleted',
                    role=Role.objects.get(name=instance.name)
                )
            self.perform_destroy(instance)
            print(event)
            return JsonResponse({"success": f'Object {pk} Deleted'})
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Object Does Not Exist'})     
        except:
            print("Unexpected errors:", type(sys.exc_info()), sys.exc_info())
            return JsonResponse({"error": str(sys.exc_info())})
