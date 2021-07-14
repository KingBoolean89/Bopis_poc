from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from users.serializers import *
from resources.serializers import *
from .models import *
from resources.models import *
from auth.permissions import IsAuthenticated
from common.pagination import CustomPagination
from django.core.exceptions import ObjectDoesNotExist
import sys
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_roles_resource(request, id):
    try:
        resources = list(Resource.objects.filter(roles__id=id))
        paginator = CustomPagination()
        page = paginator.paginate_queryset(resources, request)
        serializer = ResourceSerializer(page, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        return HttpResponse(status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_users_by_role(request, id):
    users = list(User.objects.filter(roles__id=id))
    paginator = CustomPagination()
    page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(page, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_by_name(request, name):
    try:
        resources = list(Resource.objects.filter(roles__name=name))
        print(resources)
        serializer = ResourceSerializer(resources, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        return HttpResponse(status=400)

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_all_resources(request, id):
    try:
        found_role = Role.objects.get(pk=id)
        print(found_role)
        found_role.resources.clear()
        return JsonResponse({"success": 1})
    except:
        return HttpResponse(status=400)    

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_roles_resource(request,roleID, id):
    try:
        found_role = Role.objects.get(pk=roleID)
        print(found_role)
        found_resources = Resource.objects.get(pk=id)
        print(found_resources)
        found_role.resources.remove(found_resources)
        return JsonResponse({"success": 1})
    except:
        return HttpResponse(status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_all_role_by_resource(request,id):
    data = []
    roles = list(Role.objects.all())
    roles_with_resource = list(Role.objects.filter(resources__id=id))
    new_list = list(dict.fromkeys(roles_with_resource))
    print(new_list)
    for role in roles:
        if role in new_list:
            setattr(role, 'has_access', True)
            data.append(role)
        else:
             setattr(role, 'has_access', False)
             data.append(role)
    paginator = CustomPagination()
    context = paginator.paginate_queryset(data, request)
    serializer = RoleAccessSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def can_delete_role(self, id):
    try:
        role = Role.objects.get(pk=id)
        users = list(User.objects.all())
        users_with_role = list(User.objects.filter(roles__id=id))
        print(users_with_role)
        if not users_with_role:
            response = {
                'Response': True
            }
        else:
            response = {
                'Response': False
            }
        return Response(data=response)  
    except ObjectDoesNotExist:
        return JsonResponse({"error": 'Object Does Not Exist'})     
    except:
        print("Unexpected errors:", type(sys.exc_info()), sys.exc_info())
        return JsonResponse({"error": str(sys.exc_info())})