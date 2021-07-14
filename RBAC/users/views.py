from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
import sys
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .serializers import *
from roles.serializers import *
from roles.models import *
from events.models import *
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes =[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    ordering_fields = [
        'id', 
        'username', 
        'roles'
        ]
    search_fields = [
        'id', 
        'username', 
        'roles'
        ]
    filterset_fields = [
        'id', 
        'username', 
        'roles__name',
        ]

    def partial_update(self, request, pk, *args, **kwargs):
        data = request.data
        roles = data['roles']
        print(roles)
        found_user = User.objects.get(pk=pk)
        for role in roles:
            print(role)
            role_obj = Role.objects.get(id=role)
            found_user.roles.add(role_obj)
        serializer = UserSerializer(found_user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        event = Event( 
            timestamp=now(),
            action='User Updated',
            user=User.objects.get(username=found_user.username)
        )
        event.save()
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        roles = data['roles']
        print(roles)
        if data == False:
            return HttpResponse(status=400)
        else:
            new_user = User.objects.create(
                username=data['username'],
                password=data['password'],
            )
            new_user.save()
            event = Event( 
            timestamp=now(),
            action='User Created',
            user=User.objects.get(username=data['username'])
            )
            event.save()
            for role in roles:
                role_obj = Role.objects.get(name=role)
                new_user.roles.add(role_obj)
                new_user.save()
            serializer = UserSerializer(new_user)
            return Response(serializer.data)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            instance = self.get_object()
            event = Event( 
                    timestamp=now(),
                    action='User Deleted',
                    user=User.objects.get(username=instance.username)
                )
            self.perform_destroy(instance)
            print(event)
            return JsonResponse({"success": f'Object {pk} Deleted'})
        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Object Does Not Exist'})     
        except:
            print("Unexpected errors:", type(sys.exc_info()), sys.exc_info())
            return JsonResponse({"error": str(sys.exc_info())})
