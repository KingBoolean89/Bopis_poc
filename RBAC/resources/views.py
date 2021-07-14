from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
import sys
from django.db import IntegrityError
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
from events.models import *
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination

class ResourceViewset(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    pagination_class = CustomPagination
    permission_classes =[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    ordering_fields = ['name']
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        try:
            if data == False:
                return HttpResponse(status=400)
            else:
                resource = Resource.objects.create(
                    name=data['name'],
                )
                serializer = ResourceSerializer(resource, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                event = Event( 
                    timestamp=now(),
                    action='Resource Created',
                    resource=Resource.objects.get(name=data['name'])
                )
                event.save()
                print(event)
                return Response(serializer.data)
        except IntegrityError:
            return HttpResponse(status=400)

    def partial_update(self, request, pk, *args, **kwargs):
        data = request.data
        try:
            resource = Resource.objects.get(id=pk)
            print(resource)
            serializer = ResourceSerializer(resource,data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            event = Event( 
                    timestamp=now(),
                    action='Resource Updated',
                    resource=Resource.objects.get(pk=resource.id)
                )
            event.save()
            print(event)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Resource Does Not Exist'}) 
        except IntegrityError: 
            return HttpResponse(status=400)

        

    def destroy(self, request, pk, *args, **kwargs):
        try:
            instance = self.get_object()
            event = Event( 
                    timestamp=now(),
                    action='Resource Deleted',
                    resource=Resource.objects.get(name=instance.name)
                )
            self.perform_destroy(instance)
            print(event)
            return JsonResponse({"success": f'Object {pk} Deleted'})
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Object Does Not Exist'})     
        except:
            print("Unexpected errors:", type(sys.exc_info()), sys.exc_info())
            return JsonResponse({"error": str(sys.exc_info())})
